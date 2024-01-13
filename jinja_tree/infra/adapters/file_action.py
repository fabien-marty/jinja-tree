from typing import Optional

from jinja_tree.app.config import Config
from jinja_tree.app.file_action import (
    FileAction,
    FileActionPort,
    IgnoreFileAction,
    ProcessFileAction,
)

DEFAULT_EXTENSIONS = [".template"]


class ExtensionsFileActionAdapter(FileActionPort):
    def __init__(self, config: Config):
        self.config = config
        self.extensions = config.file_action_plugin_config.get(
            "extensions", DEFAULT_EXTENSIONS
        )

    def get_action(self, absolute_path: str) -> FileAction:
        target_absolute_path: Optional[str] = None
        for extension in self.extensions:
            if absolute_path.endswith(extension):
                target_absolute_path = absolute_path[0 : -(len(extension))]
                break
        if target_absolute_path is None:
            # break not encountered
            return IgnoreFileAction(source_absolute_path=absolute_path)
        return ProcessFileAction(
            source_absolute_path=absolute_path,
            target_absolute_path=target_absolute_path,
            delete_original=self.config.delete_original,
        )
