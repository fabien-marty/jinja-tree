import os

import pytest

from jinja_tree.app.config import Config
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
    config.context_plugin_config["env_ignores"] = ["F*", "PYTEST_*"]
    config.context_plugin_config["plugin_configuration_ignores"] = ["*"]
    config.context_plugin_config["dotenv_ignores"] = ["*"]
    x = EnvContextAdapter(config)
    assert x.get_context() == {"BAR": "FOO"}


def test_config_file():
    config = Config()
    config.context_plugin_config["foo"] = "bar"
    config.context_plugin_config["env_ignores"] = ["*"]
    config.context_plugin_config["dotenv_ignores"] = ["*"]
    x = EnvContextAdapter(config)
    assert x.get_context() == {"foo": "bar"}
