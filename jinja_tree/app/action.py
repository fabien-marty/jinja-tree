import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

import stlog

from jinja_tree.app.config import Config

logger = stlog.getLogger("jinja-tree")


@dataclass
class FileAction:
    """Abstract base class for file actions.

    Attributes:
        source_absolute_path: absolute path for the source file (the template).
    """

    source_absolute_path: str

    @property
    def dirpath(self) -> str:
        return os.path.dirname(self.source_absolute_path)


@dataclass
class IgnoreFileAction(FileAction):
    """This is a concrete implementation of FileAction to represent a "do nothing with this file" action."""

    pass


@dataclass
class ProcessFileAction(FileAction):
    """This is a concrete implementation of FileAction to represent a "process this file with jinja" action.

    Attributes:
        target_absolute_path: absolute path for the target file (the rendered file).
        delete_original: if True, the original file will be deleted after the rendering.
    """

    target_absolute_path: str
    delete_original: bool = False


@dataclass
class RenameFileAction(FileAction):
    """This is a concrete implementation of fileAction to represent a "rename this file" action."""

    target_absolute_path: str


@dataclass
class DirectoryAction:
    """Abstract base class for directory actions.

    Attributes:
        source_absolute_path: absolute path for the source directory.
    """

    source_absolute_path: str


@dataclass
class IgnoreDirectoryAction(DirectoryAction):
    """This is a concrete implementation of DirectoryAction to represent a "do nothing with this directory" action.

    All files in this directory or subdirectories will be ignored (recursively).
    """

    pass


@dataclass
class BrowseDirectoryAction(DirectoryAction):
    """This is a concrete implementation of DirectoryAction to represent a "browse this directory" action.

    The directory itself won't be changed but all files and subdirectories will be scanned for actions.
    """

    pass


CONCRETE_DIRECTORY_ACTIONS = [IgnoreDirectoryAction, BrowseDirectoryAction]
CONCRETE_FILE_ACTIONS = [IgnoreFileAction, ProcessFileAction, RenameFileAction]


class ActionPort(ABC):
    """This is the abstract interface for FileActionPort adapters."""

    @abstractmethod
    def __init__(self, config: Config):
        """
        Construct a new FileActionPort object given a configuration object.

        The "action" plugin configuration block is available in:
        config.action_plugin_config

        Args:
            config (Config): The configuration object.
        """
        pass

    @abstractmethod
    def get_file_action(self, absolute_path: str) -> FileAction:
        """Return the action to execute on the file at the given absolute path.

        Note:
        - absolute_path is checked to be a file before calling this method.

        Attributes:
            absolute_path: absolute path for the file to process.
        """
        pass

    @abstractmethod
    def get_directory_action(self, absolute_path: str) -> DirectoryAction:
        """Return the action to execute on the directory at the given absolute path.

        Note:
        - absolute_path is checked to be a directory before calling this method.

        Attributes:
            absolute_path: absolute path for the directory to process.
        """
        pass


class ActionService:
    """This service is responsible for returning the action to execute on the file at the given absolute path.

    It's a kind of proxy object on FileActionPort adapters to factorize some common logic.

    Attributes:
        config: The configuration object.
        adapter: The FileActionPort adapter to use.

    """

    def __init__(self, config: Config, adapter: ActionPort):
        self.config = config
        self.adapter = adapter

    def get_file_action(self, absolute_path: str) -> FileAction:
        """Return the action to execute on the file at the given absolute path.

        Attributes:
            absolute_path: absolute path for the file to process.
        """
        assert os.path.isfile(absolute_path)
        action = self.adapter.get_file_action(absolute_path)
        if not hasattr(action, "target_absolute_path"):
            return action
        if os.path.exists(action.target_absolute_path) and not os.path.isfile(
            action.target_absolute_path
        ):
            logger.warning(
                f"target file: {action.target_absolute_path} is not a file => ignoring"
            )
            return IgnoreFileAction(source_absolute_path=absolute_path)

        return action

    def get_directory_action(self, absolute_path: str) -> DirectoryAction:
        """Return the action to execute on the directory at the given absolute path.

        Attributes:
            absolute_path: absolute path for the directory to process.
        """
        assert os.path.isdir(absolute_path)
        return self.adapter.get_directory_action(absolute_path)
