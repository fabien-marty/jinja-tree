import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Annotated, List, Optional

import stlog
import tomli
import typer

from jinja_tree.app.config import (
    Config,
    make_default_context_plugin_config,
    make_default_file_action_plugin_config,
)
from jinja_tree.infra.utils import get_config_file_path

ConfigFileType = Annotated[
    Optional[str],
    typer.Option(
        help="config file path (default: first '.jinja-tree.toml' file found up from current working dir), can also be see with JINJA_TREE_CONFIG_FILE env var"
    ),
]
LogLevelType = Annotated[
    Optional[str], typer.Option(help="log level (DEBUG, INFO, WARNING or ERROR)")
]

ExtraSearchPathsType = Annotated[
    Optional[List[Path]], typer.Option(help="Search path to jinja")
]

AddProcessedFileDirToSearchPathType = Annotated[
    Optional[bool],
    typer.Option(help="add directory of current processed file to jinja search path"),
]

AddRootDirToSearchPathType = Annotated[
    Optional[bool], typer.Option(help="add root directory to jinja search path")
]

AddCwdDirToSearchPathType = Annotated[
    Optional[bool],
    typer.Option(help="add current working directory (CWD) to jinja search path"),
]

ExtensionType = Annotated[
    Optional[List[str]], typer.Option(help="jinja extension to load")
]

ContextPluginType = Annotated[
    Optional[str], typer.Option(help="context plugin (full python class path)")
]

StrictUndefinedType = Annotated[
    Optional[bool],
    typer.Option(help="if set, raise an error if a variable does not exist in context"),
]

FileActionPluginType = Annotated[
    Optional[str], typer.Option(help="file-action plugin (full python class path)")
]

BlankRunType = Annotated[
    bool,
    typer.Option(
        help="if set, execute a blank run (without modifying or deleting anything)"
    ),
]

ReplaceType = Annotated[
    Optional[bool], typer.Option(help="replace target file event if exists")
]

DeleteOriginalType = Annotated[
    Optional[bool], typer.Option(help="delete original file")
]

DisableEmbeddedExtensions = Annotated[
    Optional[bool], typer.Option(help="disable embedded jinja extensions")
]


RootDirType = Annotated[Path, typer.Argument(help="root directory")]


def get_config(
    config_file_path: ConfigFileType = None,
    extra_search_path: ExtraSearchPathsType = None,
    add_cwd_to_search_path: AddCwdDirToSearchPathType = None,
    add_root_dir_to_search_path: AddRootDirToSearchPathType = None,
    strict_undefined: StrictUndefinedType = None,
    jinja_extension: ExtensionType = None,
    replace: ReplaceType = None,
    delete_original: DeleteOriginalType = None,
    disable_embedded_jinja_extensions: DisableEmbeddedExtensions = None,
    root_dir: Optional[RootDirType] = None,
    context_plugin: ContextPluginType = None,
    file_action_plugin: FileActionPluginType = None,
) -> Config:
    if not config_file_path:
        config_file_path = get_config_file_path()
    general = {}
    context_plugin_config = make_default_context_plugin_config()
    file_action_plugin_config = make_default_file_action_plugin_config()
    if config_file_path:
        with open(config_file_path, "rb") as f:
            data = tomli.load(f)
        general = data.get("general", {})
        context_plugin_config = {**context_plugin_config, **data.get("context", {})}
        file_action_plugin_config = {
            **file_action_plugin_config,
            **data.get("file-action", {}),
        }
    config = Config(
        **general,
        context_plugin_config=context_plugin_config,
        file_action_plugin_config=file_action_plugin_config,
    )
    if extra_search_path:
        config.extra_search_paths = [str(x) for x in extra_search_path]
    if add_cwd_to_search_path is not None:
        config.add_cwd_to_search_path = add_cwd_to_search_path
    if add_root_dir_to_search_path is not None:
        config.add_root_dir_to_search_path = add_root_dir_to_search_path
    if strict_undefined is not None:
        config.strict_undefined = strict_undefined
    if jinja_extension:
        config.jinja_extensions = jinja_extension
    if replace is not None:
        config.replace = replace
    if delete_original is not None:
        config.delete_original = delete_original
    if disable_embedded_jinja_extensions is not None:
        config.disable_embedded_jinja_extensions = disable_embedded_jinja_extensions
    if root_dir is not None:
        config.root_dir = str(root_dir)
    if context_plugin is not None:
        config.context_plugin_config["plugin"] = context_plugin
    if file_action_plugin is not None:
        config.file_action_plugin_config["plugin"] = file_action_plugin
    config.__post_init__()
    return config


def config_dump(config: Config):
    print("<config dump>", file=sys.stderr)
    print(json.dumps(asdict(config), indent=4, sort_keys=True), file=sys.stderr)
    print("</config dump>", file=sys.stderr)


def setup_logger(log_level: Optional[str]):
    if log_level is None:
        log_level = "INFO"
    stlog.setup(level=log_level)
