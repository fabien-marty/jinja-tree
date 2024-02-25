import os

import pytest

from jinja_tree.app.config import Config
from jinja_tree.infra.adapters.context import (
    ConfigurationContextAdapter,
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


def test_config_file():
    config = Config()
    x = ConfigurationContextAdapter(config, {"foo": "bar"})
    assert x.get_context() == {"foo": "bar"}
