import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

EMBEDDED_EXTENSIONS = [
    "jinja_tree.app.embedded_extensions.from_json.FromJsonExtension",
    "jinja_tree.app.embedded_extensions.shell.ShellExtension",
    "jinja_tree.app.embedded_extensions.fnmatch.FnMatchExtension",
    "jinja_tree.app.embedded_extensions.double_quotes.DoubleQuotesExtension",
    "jinja_tree.app.embedded_extensions.urlencode.UrlEncodeExtension",
]

JINJA_TREE_URL = "https://github.com/fabien-marty/jinja-tree"


def make_default_context_plugins() -> List[str]:
    return [
        "jinja_tree.infra.adapters.context.ConfigurationContextAdapter",
        "jinja_tree.infra.adapters.context.EnvContextAdapter",
        "jinja_tree.infra.adapters.context.DotEnvContextAdapter",
    ]


def make_default_action_plugins() -> List[str]:
    return ["jinja_tree.infra.adapters.action.ExtensionsFileActionAdapter"]


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
    context_generated_comment_line1: str = "*** GENERATED FILE - DO NOT EDIT ***"
    context_generated_comment_line2: str = (
        "This file was generated by jinja-tree (%s) from the template file: {{relative_filepath}}"
        % JINJA_TREE_URL
    )
    context_plugins: List[str] = field(default_factory=make_default_context_plugins)
    action_plugins: List[str] = field(default_factory=make_default_action_plugins)

    context_plugins_configs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    action_plugins_configs: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @property
    def resolved_extensions(self) -> List[str]:
        if self.disable_embedded_jinja_extensions:
            return self.jinja_extensions
        return EMBEDDED_EXTENSIONS + self.jinja_extensions

    def __post_init__(self):
        # replaces paths by absolute paths
        self.root_dir = os.path.abspath(self.root_dir)
        self.extra_search_paths = [os.path.abspath(x) for x in self.extra_search_paths]
