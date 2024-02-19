import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List

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
DEFAULT_CONCRETE_DIRECTORY_ACTION = BrowseDirectoryAction
CONCRETE_FILE_ACTIONS = [IgnoreFileAction, ProcessFileAction, RenameFileAction]
DEFAULT_CONCRETE_FILE_ACTION = IgnoreFileAction


class ActionPort(ABC):
    """This is the abstract interface for FileActionPort adapters."""

    @abstractmethod
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        """
        Construct a new FileActionPort object given a configuration object
        and a plugin configuration dict.

        Args:
            config (Config): The configuration object.
            plugin_config (Dict[str, Any]): The plugin configuration dict.

        """
        pass

    @classmethod
    @abstractmethod
    def get_config_name(cls) -> str:
        """
        Return the name of the configuration object.

        For example, if we return "foo", it means that the configuration in the TOML file
        is located under:

        [action.foo]
        # ... some configuration ...

        Returns:
            The name of the configuration object.

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

    def __init__(self, config: Config, adapters: List[ActionPort]):
        self.config = config
        self.adapters = adapters

    def get_file_action(self, absolute_path: str) -> FileAction:
        """Return the action to execute on the file at the given absolute path.

        Attributes:
            absolute_path: absolute path for the file to process.
        """
        assert os.path.isfile(absolute_path)
        if not self.adapters:
            raise Exception("no action plugins configured!")
        for adapter in self.adapters:
            a = adapter.get_file_action(absolute_path)
            if not isinstance(a, tuple(CONCRETE_FILE_ACTIONS)):
                raise Exception(f"bad action: {a} returned by action plugin: {adapter}")
            if isinstance(a, DEFAULT_CONCRETE_FILE_ACTION):
                # => IgnoreFileAction, let's try next adapter
                continue
            target_absolute_path: str = a.target_absolute_path  # type: ignore
            if os.path.exists(target_absolute_path) and not os.path.isfile(
                target_absolute_path
            ):
                logger.warning(
                    f"target file: {target_absolute_path} is not a file => ignoring"
                )
                return IgnoreFileAction(source_absolute_path=absolute_path)
            return a
        return DEFAULT_CONCRETE_FILE_ACTION(source_absolute_path=absolute_path)

    def get_directory_action(self, absolute_path: str) -> DirectoryAction:
        """Return the action to execute on the directory at the given absolute path.

        Attributes:
            absolute_path: absolute path for the directory to process.
        """
        assert os.path.isdir(absolute_path)
        for adapter in self.adapters:
            a = adapter.get_directory_action(absolute_path)
            if not isinstance(a, tuple(CONCRETE_DIRECTORY_ACTIONS)):
                raise Exception(f"bad action: {a} returned by action plugin: {adapter}")
            if isinstance(a, DEFAULT_CONCRETE_DIRECTORY_ACTION):
                # => BrowseDirectoryAction, let's try next adapter
                continue
            return a
        return DEFAULT_CONCRETE_DIRECTORY_ACTION(source_absolute_path=absolute_path)
