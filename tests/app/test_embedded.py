import json

from jinja2 import Environment

from jinja_tree.app.config import Config
from jinja_tree.app.context import ContextPort, ContextService
from jinja_tree.app.jinja import JinjaService


class MockContextAdapter(ContextPort):
    def __init__(self, config: Config, plugin_config: dict[str, object]):
        pass

    def get_context(self, absolute_path: str | None = None) -> dict[str, object]:
        return {}

    @classmethod
    def get_config_name(cls) -> str:
        return "mock"


def test_shell():
    env = Environment(
        extensions=["jinja_tree.app.embedded_extensions.shell.ShellExtension"]
    )
    template = env.from_string('test {{ "whoami"|shell }}')
    result = template.render()
    assert len(result) >= 6


def test_shell_input():
    env = Environment(
        extensions=["jinja_tree.app.embedded_extensions.shell.ShellExtension"]
    )
    template = env.from_string("{{ 'cat' | shell(input='meow', text=true) }}")
    result = template.render()
    assert result == "meow"


def test_from_json():
    env = Environment(
        extensions=["jinja_tree.app.embedded_extensions.from_json.FromJsonExtension"]
    )
    x = ["foo", "bar"]
    template = env.from_string(
        "test {% set y = '" + json.dumps(x) + "'|from_json %} {{'bar' in y}}"
    )
    result = template.render()
    assert result == "test  True"
    x = ["foo", "foo2"]
    template = env.from_string(
        "test {% set y = '" + json.dumps(x) + "'|from_json %} {{'bar' in y}}"
    )
    result = template.render()
    assert result == "test  False"


def test_from_toml():
    env = Environment(
        extensions=["jinja_tree.app.embedded_extensions.from_toml.FromTomlExtension"]
    )
    toml = """
[foo]
bar = "baz"
"""
    template = env.from_string(
        "test {% set y = '" + toml + "'|from_toml %} {{'foo' in y}}"
    )
    result = template.render()
    assert result == "test  True"


def test_fnmatch():
    env = Environment(
        extensions=["jinja_tree.app.embedded_extensions.fnmatch.FnMatchExtension"]
    )
    template = env.from_string('test {{ "foo-bar"|fnmatch("foo-*") }}')
    result = template.render()
    assert result == "test True"


def test_urlencode():
    env = Environment(
        extensions=["jinja_tree.app.embedded_extensions.urlencode.UrlEncodeExtension"]
    )
    template = env.from_string('test {{ "https://google.com"|urlencode(safe="") }}')
    result = template.render()
    assert result == "test https%3A%2F%2Fgoogle.com"


def test_counter_default_start():
    env = Environment(
        extensions=["jinja_tree.app.embedded_extensions.counter.CounterExtension"]
    )
    template = env.from_string("{{ counter() }} {{ counter() }} {{ counter() }}")
    result = template.render()
    assert result == "0 1 2"


def test_counter_custom_start_first_call():
    env = Environment(
        extensions=["jinja_tree.app.embedded_extensions.counter.CounterExtension"]
    )
    template = env.from_string(
        "{{ counter(start=3) }} {{ counter() }} {{ counter() }}"
    )
    result = template.render()
    assert result == "3 4 5"


def test_counter_named_counters_are_independent():
    env = Environment(
        extensions=["jinja_tree.app.embedded_extensions.counter.CounterExtension"]
    )
    template = env.from_string(
        "{{ counter() }} {{ counter(name='foo') }} {{ counter() }} "
        "{{ counter(name='foo') }} {{ counter(name='bar') }} {{ counter(name='bar') }}"
    )
    result = template.render()
    assert result == "0 0 1 1 0 1"


def test_counter_named_start_applies_per_name():
    env = Environment(
        extensions=["jinja_tree.app.embedded_extensions.counter.CounterExtension"]
    )
    template = env.from_string(
        "{{ counter(name='foo', start=3) }} {{ counter(name='foo') }} "
        "{{ counter() }} {{ counter(name='bar', start=7) }} {{ counter(name='bar') }}"
    )
    result = template.render()
    assert result == "3 4 0 7 8"


def test_counter_resets_between_renders():
    config = Config()
    context_adapter = MockContextAdapter(config, {})
    context_service = ContextService(config, [context_adapter])
    jinja_service = JinjaService(config, context_service)

    first_result = jinja_service.render_string("{{ counter() }} {{ counter() }}")
    second_result = jinja_service.render_string("{{ counter() }} {{ counter() }}")

    assert first_result == "0 1"
    assert second_result == "0 1"
