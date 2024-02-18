import os

import pytest

from jinja_tree.app.action import IgnoreFileAction, ProcessFileAction
from jinja_tree.app.config import Config
from jinja_tree.infra.adapters.action import ExtensionsFileActionAdapter
from jinja_tree.infra.adapters.context import (
    EnvContextAdapter,
)


@pytest.fixture()
def fake_env_fixture():
    old_env = {x: y for x, y in os.environ.items()}
    os.environ.clear()
    os.environ["FOO"] = "BAR"
    os.environ["BAR"] = "FOO"
    yield
    os.environ.clear()
    for x, y in old_env.items():
        os.environ[x] = y


def test_env(fake_env_fixture):
    config = Config()
    x = EnvContextAdapter(config, {"ignores": ["F*", "PYTEST_*"]})
    assert x.get_context() == {"BAR": "FOO"}


def test_extensions():
    config = Config()
    plugin_config = {"extensions": [".template"], "delete_original": True}
    x = ExtensionsFileActionAdapter(config, plugin_config)
    a = x.get_file_action("/foo/bar/foo.template")
    assert isinstance(a, ProcessFileAction)
    assert a.source_absolute_path == "/foo/bar/foo.template"
    assert a.target_absolute_path == "/foo/bar/foo"
    assert a.delete_original is True
    a = x.get_file_action("/foo/bar/foo.py")
    assert isinstance(a, IgnoreFileAction)
    assert a.source_absolute_path == "/foo/bar/foo.py"
