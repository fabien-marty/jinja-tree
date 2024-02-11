import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

CONTEXT_PLUGIN_DEFAULT = "jinja_tree.infra.adapters.context.EnvContextAdapter"
FILE_ACTION_PLUGIN_DEFAULT = (
    "jinja_tree.infra.adapters.action.ExtensionsFileActionAdapter"
)
FILENAME_IGNORES_DEFAULT = [".*"]
DIRNAME_IGNORES_DEFAULT = [
    "venv",
    "site-packages",
    "__pypackages__",
    "node_modules",
    "__pycache__",
    ".*",
]
DOTENV_PATH_DEFAULT = ".env"
FILE_ACTION_PLUGIN_DEFAULT_EXTENSIONS = [".template"]
REPLACE_DEFAULT = True
DELETE_ORIGINAL_DEFAULT = False

EMBEDDED_EXTENSIONS = [
    "jinja_tree.app.embedded_extensions.from_json.FromJsonExtension",
    "jinja_tree.app.embedded_extensions.shell.ShellExtension",
    "jinja_tree.app.embedded_extensions.fnmatch.FnMatchExtension",
    "jinja_tree.app.embedded_extensions.double_quotes.DoubleQuotesExtension",
    "jinja_tree.app.embedded_extensions.urlencode.UrlEncodeExtension",
]

JINJA_TREE_URL = "https://github.com/fabien-marty/jinja-tree"


def make_default_context_plugin_config() -> Dict[str, Any]:
    tmp = {
        "plugin": CONTEXT_PLUGIN_DEFAULT,
        "generated_comment_line1": "*** GENERATED FILE - DO NOT EDIT ***",
        "generated_comment_line2": "This file was generated by jinja-tree (%s) from the template file: {{relative_filepath}}"
        % JINJA_TREE_URL,
        "env_ignores": [],
        "dotenv_path": DOTENV_PATH_DEFAULT,
        "dotenv_ignores": [],
    }
    tmp["plugin_configuration_ignores"] = list(tmp.keys()) + [
        "plugin_configuration_ignores"
    ]
    tmp["plugin_configuration_ignores"] = list(tmp.keys())
    return tmp


def make_default_action_plugin_config() -> Dict[str, Any]:
    return {
        "plugin": FILE_ACTION_PLUGIN_DEFAULT,
        "extensions": FILE_ACTION_PLUGIN_DEFAULT_EXTENSIONS,
        "filename_ignores": FILENAME_IGNORES_DEFAULT,
        "dirname_ignores": DIRNAME_IGNORES_DEFAULT,
        "replace": REPLACE_DEFAULT,
        "delete_original": DELETE_ORIGINAL_DEFAULT,
    }


@dataclass
class Config:
    # Global config
    extra_search_paths: List[str] = field(default_factory=list)
    add_root_dir_to_search_path: bool = True
    add_cwd_to_search_path: bool = True
    add_processed_file_dir_to_search_path: bool = False
    change_cwd: bool = True
    jinja_extensions: List[str] = field(default_factory=list)
    strict_undefined: bool = True
    root_dir: str = field(default_factory=os.getcwd)
    disable_embedded_jinja_extensions: bool = False
    verbose: bool = False
    log_level: str = "INFO"

    # Plugin config
    context_plugin_config: Dict[str, Any] = field(
        default_factory=make_default_context_plugin_config
    )
    action_plugin_config: Dict[str, Any] = field(
        default_factory=make_default_action_plugin_config
    )

    @property
    def resolved_extensions(self) -> List[str]:
        if self.disable_embedded_jinja_extensions:
            return self.jinja_extensions
        return EMBEDDED_EXTENSIONS + self.jinja_extensions

    def __post_init__(self):
        # replaces paths by absolute paths
        self.root_dir = os.path.abspath(self.root_dir)
        self.extra_search_paths = [os.path.abspath(x) for x in self.extra_search_paths]
