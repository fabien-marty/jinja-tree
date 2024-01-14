import os

import pytest

from jinja_tree.app.config import Config
from jinja_tree.app.context import ContextPort
from jinja_tree.app.file_action import FileActionPort
from jinja_tree.infra.utils import (
    get_config_file_path,
    is_fnmatch_ignored,
    make_context_adapter_from_config,
    make_file_action_adapter_from_config,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")


def test_make_context_adapter_from_config():
    adapter = make_context_adapter_from_config(config=Config())
    assert isinstance(adapter, ContextPort)


def test_make_file_action_adapter_from_config():
    adapter = make_file_action_adapter_from_config(config=Config())
    assert isinstance(adapter, FileActionPort)


@pytest.fixture
def dir2_cwd_fixture():
    old_cwd = os.getcwd()
    os.chdir(os.path.join(DATA_DIR, "dir1", "dir2"))
    yield old_cwd
    os.chdir(old_cwd)


def test_get_config_file_path(dir2_cwd_fixture):
    path = get_config_file_path()
    assert path == os.path.join(DATA_DIR, "dir1", ".jinja-tree.toml")
    path = get_config_file_path(cli_option="foo")
    assert path == "foo"
    path = get_config_file_path(cwd=os.path.join(SCRIPT_DIR, "..", "..", ".."))
    assert path is None


def test_is_fnmatch_ignored():
    ignores = ["*.txt", "test_*"]
    assert is_fnmatch_ignored("file.txt", ignores) is True
    assert is_fnmatch_ignored("test_file.py", ignores) is True
    assert is_fnmatch_ignored("file.py", ignores) is False
