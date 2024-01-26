import fnmatch
import os
from importlib import import_module
from typing import List, Optional, Type

import stlog

from jinja_tree.app.action import ActionPort
from jinja_tree.app.config import (
    CONTEXT_PLUGIN_DEFAULT,
    FILE_ACTION_PLUGIN_DEFAULT,
    Config,
)
from jinja_tree.app.context import ContextPort

SYSTEM_CONFIG_PATH = "/etc/jinja-tree.toml"

logger = stlog.getLogger("jinja_tree")


def import_class_from_string(class_path: str) -> Type:
    module_name, _, class_name = class_path.rpartition(".")
    klass = getattr(import_module(module_name), class_name)
    return klass


def make_context_adapter_from_config(config: Config) -> ContextPort:
    class_path = config.context_plugin_config.get("plugin", CONTEXT_PLUGIN_DEFAULT)
    context_adapter_class = import_class_from_string(class_path)
    context_adapter = context_adapter_class(config=config)
    if not isinstance(context_adapter, ContextPort):
        raise Exception(
            f"the class pointed by {class_path} does not implement ContextPort interface"
        )
    return context_adapter


def make_file_action_adapter_from_config(config: Config) -> ActionPort:
    class_path = config.action_plugin_config.get("plugin", FILE_ACTION_PLUGIN_DEFAULT)
    context_adapter_class = import_class_from_string(class_path)
    file_action_adapter = context_adapter_class(config=config)
    if not isinstance(file_action_adapter, ActionPort):
        raise Exception(
            f"the class pointed by {class_path} does not implement FileActionPort interface"
        )
    return file_action_adapter


def get_config_file_path(
    cli_option: Optional[str] = None, cwd: Optional[str] = None
) -> Optional[str]:
    if cli_option is not None:
        logger.debug(f"config file path read from CLI: {cli_option}")
        return cli_option
    if os.environ.get("JINJA_TREE_CONFIG_FILE"):
        logger.debug(
            f"config file path read from env var JINJA_TREE_CONFIG_FILE: {os.environ.get('JINJA_TREE_CONFIG_FILE')}"
        )
        return os.environ.get("JINJA_TREE_CONFIG_FILE")
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
    return any(fnmatch.fnmatch(key, x) for x in ignores)
