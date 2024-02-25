import fnmatch
import os
import sys
from importlib import import_module
from typing import List, Optional, Type

import dataclasses_json
import stlog
import tomli

from jinja_tree.app.action import ActionPort
from jinja_tree.app.config import (
    Config,
)
from jinja_tree.app.context import ContextPort

SYSTEM_CONFIG_PATH = "/etc/jinja-tree.toml"

logger = stlog.getLogger("jinja_tree")


def import_class_from_string(class_path: str) -> Type:
    module_name, _, class_name = class_path.rpartition(".")
    klass = getattr(import_module(module_name), class_name)
    return klass


def make_context_adapter_from_config(klass, config: Config) -> ContextPort:
    config_name = klass.get_config_name()
    plugin_config = config.context_plugins_configs.get(config_name, {})
    return klass(config, plugin_config)


def make_action_adapter_from_config(klass, config: Config) -> ContextPort:
    config_name = klass.get_config_name()
    plugin_config = config.action_plugins_configs.get(config_name, {})
    return klass(config, plugin_config)


def make_context_adapters_from_config(config: Config) -> List[ContextPort]:
    res: List[ContextPort] = []
    for class_path in config.context_plugins:
        context_adapter_class = import_class_from_string(class_path)
        context_adapter = make_context_adapter_from_config(
            context_adapter_class, config
        )
        if not isinstance(context_adapter, ContextPort):
            raise Exception(
                f"the class pointed by {class_path} does not implement ContextPort interface"
            )
        res.append(context_adapter)
    return res


def make_action_adapters_from_config(config: Config) -> List[ActionPort]:
    res: List[ActionPort] = []
    for class_path in config.action_plugins:
        context_adapter_class = import_class_from_string(class_path)
        action_adapter = make_action_adapter_from_config(context_adapter_class, config)
        if not isinstance(action_adapter, ActionPort):
            raise Exception(
                f"the class pointed by {class_path} does not implement ActionPort interface"
            )
        res.append(action_adapter)
    return res


def get_config_file_path(
    cli_option: Optional[str] = None, cwd: Optional[str] = None
) -> Optional[str]:
    """
    Get the path to the configuration file.

    - if the CLI option is set, it is returned immediately (note: can be set by JINJA_TREE_CONFIG_FILE env var)
    - else, we will try to find it in the current working directory
        or in the parent directory (recursively).

    Args:
        cli_option: The configuration file path provided via CLI
            (if set, the function returns this value immediately)
        cwd: The current working directory (if not set, the current working directory is used)

    Returns:
        The path to the configuration file, or None if not found.

    """
    if cli_option is not None:
        logger.debug(f"config file path read from CLI: {cli_option}")
        return cli_option
    if cwd is None:
        cwd = os.getcwd()
    else:
        cwd = os.path.abspath(cwd)
    path = os.path.join(cwd, ".jinja-tree.toml")
    if os.path.isfile(path):
        logger.debug(f"config file path found in: {path}")
        return os.path.abspath(path)
    parent_path = os.path.dirname(cwd)
    if parent_path == cwd:
        # we are done
        # let's try the system config path?
        if os.path.isfile(SYSTEM_CONFIG_PATH):
            return SYSTEM_CONFIG_PATH
        logger.debug("no config file found")
        return None
    return get_config_file_path(cwd=parent_path)


def is_fnmatch_ignored(key: str, ignores: List[str]) -> bool:
    """
    Check if the given key matches any of the patterns in the ignores list using fnmatch.

    Args:
        key: The key to check.
        ignores: The list of patterns to ignore.

    Returns:
        True if the key matches any of the patterns, False otherwise.
    """
    return any(fnmatch.fnmatch(key, x) for x in ignores)


def setup_logger(log_level: Optional[str] = None):
    if log_level is None:
        log_level = "INFO"
    stlog.setup(level=log_level)


def log_error_and_die(*args, **kwargs):
    setup_logger()  # as we are not that logging is setup at this point
    logger.error(*args, **kwargs)
    sys.exit(1)


def read_config_file_or_die(config_file_path: Optional[str]) -> Config:
    with stlog.LogContext.bind(config_file_path=config_file_path):
        if config_file_path is not None:
            try:
                with open(config_file_path, "rb") as f:
                    data = tomli.load(f)
            except Exception:
                log_error_and_die("cannot read config file", exc_info=True)
            for key in data.keys():
                if key not in ("general", "context", "action"):
                    log_error_and_die(f"invalid section: {key} found in config file")
            general = data.get("general", {})
            try:
                config = Config.from_dict(general)
            except dataclasses_json.undefined.UndefinedParameterError as e:
                log_error_and_die(
                    f"invalid parameters found in general section of the config file: {e.normalized_messages()}"
                )
            config.context_plugins_configs = data.get("context", {})
            config.action_plugins_configs = data.get("action", {})
            try:
                make_context_adapters_from_config(config)
            except dataclasses_json.undefined.UndefinedParameterError as e:
                log_error_and_die(
                    f"invalid parameters found in context section of the config file: {e.normalized_messages()}"
                )
            except Exception:
                log_error_and_die("invalid context plugin configuration", exc_info=True)
            try:
                make_action_adapters_from_config(config)
            except dataclasses_json.undefined.UndefinedParameterError as e:
                log_error_and_die(
                    f"invalid parameters found in action section of the config file: {e.normalized_messages()}"
                )
            except Exception:
                log_error_and_die("invalid action plugin configuration", exc_info=True)
            config.__post_init__()
            return config
    return Config()
