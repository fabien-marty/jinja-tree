from typing import Optional

from jinja_tree.app.config import (
    FILE_ACTION_PLUGIN_DEFAULT_EXTENSIONS,
    FILE_ACTION_PLUGIN_DEFAULT_IN_PLACE,
    Config,
)
from jinja_tree.app.file_action import (
    FileAction,
    FileActionPort,
    IgnoreFileAction,
    ProcessFileAction,
)


class ExtensionsFileActionAdapter(FileActionPort):
    def __init__(self, config: Config):
        self.config = config
        self.extensions = config.file_action_plugin_config.get(
            "extensions", FILE_ACTION_PLUGIN_DEFAULT_EXTENSIONS
        )
        self.in_place = config.file_action_plugin_config.get(
            "in_place", FILE_ACTION_PLUGIN_DEFAULT_IN_PLACE
        )
        if self.in_place:
            if self.config.delete_original:
                raise ValueError(
                    "delete_original=True is not compatible when using in_place=True"
                )

    def get_action(self, absolute_path: str) -> FileAction:
        target_absolute_path: Optional[str] = None
        for extension in self.extensions:
            if absolute_path.endswith(extension):
                if self.in_place:
                    target_absolute_path = absolute_path
                else:
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
