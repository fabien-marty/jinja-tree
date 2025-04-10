import os

import pytest

from jinja_tree.app.config import Config
from jinja_tree.infra.adapters.context import (
    ConfigurationContextAdapter,
    EnvContextAdapter,
    TOMLContextAdapter,
)

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


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


def test_config_file():
    config = Config()
    x = ConfigurationContextAdapter(config, {"foo": "bar"})
    assert x.get_context() == {"foo": "bar"}


def test_toml_file():
    config = Config()
    x = TOMLContextAdapter(
        config, {"path": os.path.join(SCRIPT_DIR, "data", "foo.toml")}
    )
    assert x.get_context() == {"key1": "value1", "key2": "value2"}


def test_toml_file_empty_config():
    config = Config()
    x = TOMLContextAdapter(config, {})
    assert x.get_context() == {}
