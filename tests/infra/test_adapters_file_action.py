import os

import pytest

from jinja_tree.app.config import Config
from jinja_tree.app.file_action import IgnoreFileAction, ProcessFileAction
from jinja_tree.infra.adapters.context import (
    EnvContextAdapter,
)
from jinja_tree.infra.adapters.file_action import ExtensionsFileActionAdapter


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
    config.context_plugin_config["env_ignores"] = ["F*", "PYTEST_*"]
    x = EnvContextAdapter(config)
    assert x.get_context() == {"BAR": "FOO"}


def test_extensions():
    x = ExtensionsFileActionAdapter(
        Config(
            delete_original=True,
            file_action_plugin_config={"extensions": [".template"]},
        )
    )
    a = x.get_action("/foo/bar/foo.template")
    assert isinstance(a, ProcessFileAction)
    assert a.source_absolute_path == "/foo/bar/foo.template"
    assert a.target_absolute_path == "/foo/bar/foo"
    assert a.delete_original is True
    a = x.get_action("/foo/bar/foo.py")
    assert isinstance(a, IgnoreFileAction)
    assert a.source_absolute_path == "/foo/bar/foo.py"
