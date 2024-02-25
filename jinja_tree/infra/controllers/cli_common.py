from pathlib import Path
from typing import List, Optional

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore

import typer

from jinja_tree.app.config import (
    Config,
)
from jinja_tree.infra.utils import get_config_file_path, read_config_file_or_die

ConfigFileType = Annotated[
    Optional[str],
    typer.Option(
        help="config file path (default: first '.jinja-tree.toml' file found up from current working dir), can also be see with JINJA_TREE_CONFIG_FILE env var",
        envvar="JINJA_TREE_CONFIG_FILE",
    ),
]
LogLevelType = Annotated[
    str, typer.Option(help="log level (DEBUG, INFO, WARNING or ERROR)")
]

ExtraSearchPathsType = Annotated[
    Optional[List[Path]],
    typer.Option(help="Search path to jinja (can be used multiple times)"),
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

ContextPluginsType = Annotated[
    Optional[List[str]],
    typer.Option(
        help="context plugins (full python class path, can be used multiple times)"
    ),
]

StrictUndefinedType = Annotated[
    Optional[bool],
    typer.Option(help="if set, raise an error if a variable does not exist in context"),
]

ActionPluginType = Annotated[
    Optional[List[str]],
    typer.Option(
        help="action plugin (full python class path, can be used multiple times)"
    ),
]

BlankRunType = Annotated[
    bool,
    typer.Option(
        help="if set, execute a blank run (without modifying or deleting anything)"
    ),
]

DisableEmbeddedExtensionsType = Annotated[
    Optional[bool], typer.Option(help="disable embedded jinja extensions")
]

VerboseType = Annotated[
    bool,
    typer.Option(
        help="increase verbosity of the DEBUG log level (note: this forces log-level = DEBUG)"
    ),
]


RootDirType = Annotated[Path, typer.Argument(help="root directory")]


def get_config(
    config_file_path: ConfigFileType = None,
    extra_search_path: ExtraSearchPathsType = None,
    add_cwd_to_search_path: AddCwdDirToSearchPathType = None,
    add_root_dir_to_search_path: AddRootDirToSearchPathType = None,
    strict_undefined: StrictUndefinedType = None,
    jinja_extension: ExtensionType = None,
    disable_embedded_jinja_extensions: DisableEmbeddedExtensionsType = None,
    root_dir: Optional[RootDirType] = None,
    context_plugins: ContextPluginsType = None,
    action_plugins: ActionPluginType = None,
    verbose: VerboseType = False,
    log_level: LogLevelType = "INFO",
) -> Config:
    if not config_file_path:
        config_file_path = get_config_file_path()
    config = read_config_file_or_die(config_file_path)
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
    if disable_embedded_jinja_extensions is not None:
        config.disable_embedded_jinja_extensions = disable_embedded_jinja_extensions
    if root_dir is not None:
        config.root_dir = str(root_dir)
    if context_plugins:
        config.context_plugins = context_plugins
    if action_plugins:
        config.action_plugins = action_plugins
    config.verbose = verbose
    if verbose:
        config.log_level = "DEBUG"
        config.verbose = True
    else:
        config.log_level = log_level
        config.verbose = False
    config.__post_init__()
    return config
