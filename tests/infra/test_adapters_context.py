import os

import pytest

from jinja_tree.app.config import Config
from jinja_tree.infra.adapters.context import (
    ConfigurationContextAdapter,
    EnvContextAdapter,
    TOMLContextAdapter,
    _deep_merge,
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
        config, {"paths": [os.path.join(SCRIPT_DIR, "data", "foo.toml")]}
    )
    assert x.get_context() == {"key1": "value1", "key2": "value2"}


def test_toml_file_empty_config():
    config = Config()
    x = TOMLContextAdapter(config, {})
    assert x.get_context() == {}


def test_toml_file_backward_compat_path():
    """Test backward compatibility: old singular 'path' field should still work."""
    config = Config()
    x = TOMLContextAdapter(
        config, {"path": os.path.join(SCRIPT_DIR, "data", "foo.toml")}
    )
    assert x.get_context() == {"key1": "value1", "key2": "value2"}


def test_deep_merge_nested_dicts():
    base = {"a": 1, "nested": {"x": 10, "y": 20}}
    override = {"b": 2, "nested": {"y": 99, "z": 30}}
    result = _deep_merge(base, override)
    assert result == {"a": 1, "b": 2, "nested": {"x": 10, "y": 99, "z": 30}}
    # originals are not mutated
    assert base == {"a": 1, "nested": {"x": 10, "y": 20}}


def test_toml_deep_merge_multiple_files():
    """Merging multiple TOML files should deep-merge nested tables."""
    config = Config()
    x = TOMLContextAdapter(
        config,
        {
            "paths": [
                os.path.join(SCRIPT_DIR, "data", "deep1.toml"),
                os.path.join(SCRIPT_DIR, "data", "deep2.toml"),
            ]
        },
    )
    assert x.get_context() == {
        "key1": "value1",
        "key2": "value2",
        "database": {
            "host": "localhost",
            "port": 3306,
            "name": "mydb",
            "options": {
                "timeout": 30,
                "retries": 5,
                "verbose": True,
            },
        },
    }
