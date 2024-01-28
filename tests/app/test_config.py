from jinja_tree.app.config import EMBEDDED_EXTENSIONS, Config


def test_config_object():
    x = Config(jinja_extensions=["foo"])
    assert x.resolved_extensions == EMBEDDED_EXTENSIONS + ["foo"]
    x = Config(jinja_extensions=["foo"], disable_embedded_jinja_extensions=True)
    assert x.resolved_extensions == ["foo"]
