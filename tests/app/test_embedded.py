import json

from jinja2 import Environment


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
        "test {% set y = '" + json.dumps(x) + "'|from_json %} " "{{'bar' in y}}"
    )
    result = template.render()
    assert result == "test  True"
    x = ["foo", "foo2"]
    template = env.from_string(
        "test {% set y = '" + json.dumps(x) + "'|from_json %} " "{{'bar' in y}}"
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
        "test {% set y = '" + toml + "'|from_toml %} " "{{'foo' in y}}"
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
