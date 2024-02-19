import os
from typing import Any, Dict, Optional

import stlog

from jinja_tree.app.action import (
    ActionPort,
    BrowseDirectoryAction,
    DirectoryAction,
    FileAction,
    IgnoreDirectoryAction,
    IgnoreFileAction,
    ProcessFileAction,
)
from jinja_tree.app.config import Config
from jinja_tree.infra.utils import is_fnmatch_ignored

FILENAME_IGNORES_DEFAULT = [".*"]
DIRNAME_IGNORES_DEFAULT = [
    "venv",
    "site-packages",
    "__pypackages__",
    "node_modules",
    "__pycache__",
    ".*",
]

DEFAULT_EXTENSIONS = [".template"]
REPLACE_DEFAULT = True
DELETE_ORIGINAL_DEFAULT = False

logger = stlog.getLogger("jinja-tree")


class ExtensionsActionAdapter(ActionPort):
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        self.config = config
        self.plugin_config = plugin_config
        self.extensions = plugin_config.get("extensions", DEFAULT_EXTENSIONS)
        self.filename_ignores = plugin_config.get(
            "filename_ignores", FILENAME_IGNORES_DEFAULT
        )
        self.dirname_ignores = plugin_config.get(
            "dirname_ignores", DIRNAME_IGNORES_DEFAULT
        )
        self.replace = plugin_config.get("replace", REPLACE_DEFAULT)
        self.delete_original = plugin_config.get(
            "delete_original", DELETE_ORIGINAL_DEFAULT
        )

    @classmethod
    def get_config_name(self) -> str:
        return "extension"

    def trace(self, msg: str, **kwargs):
        if self.config.verbose:
            logger.debug(msg, **kwargs)

    def get_file_action(self, absolute_path: str) -> FileAction:
        if is_fnmatch_ignored(os.path.basename(absolute_path), self.filename_ignores):
            self.trace(
                "Ignored file because of ignores configuration value",
                path=absolute_path,
                filename_ignores=self.filename_ignores,
            )
            return IgnoreFileAction(source_absolute_path=absolute_path)
        target_absolute_path: Optional[str] = None
        for extension in self.extensions:
            if absolute_path.endswith(extension):
                target_absolute_path = absolute_path[0 : -(len(extension))]
        if target_absolute_path is None:
            # break not encountered
            self.trace(
                "Ignored file because of its extension",
                path=absolute_path,
                extensions=self.extensions,
            )
            return IgnoreFileAction(source_absolute_path=absolute_path)
        if os.path.exists(target_absolute_path) and not self.replace:
            logger.warning(
                f"target file: {target_absolute_path} already exists and replace config parameter is False => ignoring"
            )
            return IgnoreFileAction(source_absolute_path=absolute_path)
        return ProcessFileAction(
            source_absolute_path=absolute_path,
            target_absolute_path=target_absolute_path,
            delete_original=self.delete_original,
        )

    def get_directory_action(self, absolute_path: str) -> DirectoryAction:
        if is_fnmatch_ignored(os.path.basename(absolute_path), self.dirname_ignores):
            self.trace(
                "Ignored directory because of dirname_ignores configuration value",
                path=absolute_path,
                dirname_ignores=self.dirname_ignores,
            )
            return IgnoreDirectoryAction(source_absolute_path=absolute_path)
        return BrowseDirectoryAction(source_absolute_path=absolute_path)
