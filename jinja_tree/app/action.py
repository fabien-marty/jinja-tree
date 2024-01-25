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
    """This is a concrete implementation of FileAction to represent a "process this file" action.

    Attributes:
        target_absolute_path: absolute path for the target file (the rendered file).
        delete_original: if True, the original file will be deleted after the rendering.
    """

    target_absolute_path: str
    delete_original: bool = False


@dataclass
class RenameFileAction(FileAction):
    target_absolute_path: str


class FileActionPort(ABC):
    """This is the abstract interface for FileActionPort adapters."""

    @abstractmethod
    def __init__(self, config: Config):
        """
        Construct a new FileActionPort object given a configuration object.

        Args:
            config (Config): The configuration object.
        """
        pass

    @abstractmethod
    def get_action(self, absolute_path: str) -> FileAction:
        """Return the action to execute on the file at the given absolute path.

        Attributes:
            absolute_path: absolute path for the file to process.
        """
        pass


class FileActionService:
    """This service is responsible for returning the action to execute on the file at the given absolute path.

    It's a kind of proxy object on FileActionPort adapters to factorize some common logic.

    Attributes:
        config: The configuration object.
        adapter: The FileActionPort adapter to use.

    """

    def __init__(self, config: Config, adapter: FileActionPort):
        self.config = config
        self.adapter = adapter

    def get_action(self, absolute_path: str) -> FileAction:
        if not os.path.isfile(absolute_path):
            return IgnoreFileAction(source_absolute_path=absolute_path)
        action = self.adapter.get_action(absolute_path)
        if not isinstance(action, ProcessFileAction):
            return action
        if os.path.exists(action.target_absolute_path) and not os.path.isfile(
            action.target_absolute_path
        ):
            logger.warning(
                f"target file: {action.target_absolute_path} is not a file => ignoring"
            )
            return IgnoreFileAction(source_absolute_path=absolute_path)
        if os.path.exists(action.target_absolute_path) and not self.config.replace:
            return IgnoreFileAction(source_absolute_path=absolute_path)
        return action
