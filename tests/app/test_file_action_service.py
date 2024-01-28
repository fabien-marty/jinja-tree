import os

import pytest

from jinja_tree.app.action import (
    ActionPort,
    ActionService,
    BrowseDirectoryAction,
    DirectoryAction,
    FileAction,
    IgnoreFileAction,
    ProcessFileAction,
)
from jinja_tree.app.config import Config

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")


class MockFileActionAdapter(ActionPort):
    def __init__(self, config: Config):
        self.config = config

    def get_file_action(self, absolute_path: str) -> FileAction:
        if absolute_path == "/does/not/exist":
            raise Exception("does not exist should be ignored by FileActionService")
        if absolute_path.endswith(".template"):
            return ProcessFileAction(
                source_absolute_path=absolute_path,
                target_absolute_path=absolute_path[0 : -len(".template")],
                delete_original=False,
            )
        return IgnoreFileAction(source_absolute_path=absolute_path)

    def get_directory_action(self, absolute_path: str) -> DirectoryAction:
        return BrowseDirectoryAction(source_absolute_path=absolute_path)


def safe_unlink(path: str):
    try:
        os.unlink(path)
    except Exception:
        pass


@pytest.fixture
def foo_cleanup_fixture():
    path = os.path.join(DATA_DIR, "foo")
    safe_unlink(path)
    yield None
    safe_unlink(path)


def test_file_action_service(foo_cleanup_fixture):
    config = Config()
    adapter = MockFileActionAdapter(config)
    x = ActionService(config=config, adapter=adapter)
    assert isinstance(
        x.get_file_action(os.path.join(DATA_DIR, "foo.nomatch")), IgnoreFileAction
    )
    action = x.get_file_action(os.path.join(DATA_DIR, "foo.template"))
    assert isinstance(action, ProcessFileAction)
    assert action.target_absolute_path == os.path.join(DATA_DIR, "foo")
    action = x.get_file_action(os.path.join(DATA_DIR, "foo2.template"))
    assert isinstance(action, IgnoreFileAction)
