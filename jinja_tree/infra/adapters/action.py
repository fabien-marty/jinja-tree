import os
from typing import Optional

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
from jinja_tree.app.config import (
    DELETE_ORIGINAL_DEFAULT,
    DIRNAME_IGNORES_DEFAULT,
    FILE_ACTION_PLUGIN_DEFAULT_EXTENSIONS,
    FILENAME_IGNORES_DEFAULT,
    REPLACE_DEFAULT,
    Config,
)
from jinja_tree.infra.utils import is_fnmatch_ignored

IGNORE_FILENAME = ".jinja-tree-ignore"

logger = stlog.getLogger("jinja-tree")


class ExtensionsFileActionAdapter(ActionPort):
    def __init__(self, config: Config):
        self.config = config
        self.extensions = config.action_plugin_config.get(
            "extensions", FILE_ACTION_PLUGIN_DEFAULT_EXTENSIONS
        )
        self.filename_ignores = config.action_plugin_config.get(
            "filename_ignores", FILENAME_IGNORES_DEFAULT
        )
        self.dirname_ignores = config.action_plugin_config.get(
            "dirname_ignores", DIRNAME_IGNORES_DEFAULT
        )
        self.replace = config.action_plugin_config.get("replace", REPLACE_DEFAULT)
        self.delete_original = config.action_plugin_config.get(
            "delete_original", DELETE_ORIGINAL_DEFAULT
        )

    def get_file_action(self, absolute_path: str) -> FileAction:
        if is_fnmatch_ignored(os.path.basename(absolute_path), self.filename_ignores):
            logger.debug(
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
            logger.debug(
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
            logger.debug(
                "Ignored directory because of dirname_ignores configuration value",
                path=absolute_path,
                dirname_ignores=self.dirname_ignores,
            )
            return IgnoreDirectoryAction(source_absolute_path=absolute_path)
        exclude_file = os.path.join(absolute_path, IGNORE_FILENAME)
        if os.path.isfile(exclude_file):
            logger.debug(f"{IGNORE_FILENAME} found", path=absolute_path)
            return IgnoreDirectoryAction(source_absolute_path=absolute_path)
        return BrowseDirectoryAction(source_absolute_path=absolute_path)
