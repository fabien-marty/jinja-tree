from typing import Any, Optional

import pytest
from jinja2 import UndefinedError

from jinja_tree.app.config import Config
from jinja_tree.app.context import ContextPort, ContextService
from jinja_tree.app.jinja import JinjaService


class MockContextAdapter(ContextPort):
    def __init__(self, config: Config):
        pass

    def get_context(self, absolute_path: Optional[str] = None) -> dict[str, Any]:
        return {"foo": "bar"}


def test_jinja_service():
    config = Config(strict_undefined=True)
    context_adapter = MockContextAdapter(config)
    context_service = ContextService(config, context_adapter)
    x = JinjaService(config, context_service)
    res = x.render_string("foo{{ foo }}")
    assert res == "foobar"
    with pytest.raises(UndefinedError):
        x.render_string("foo{{ bar }}")
    config = Config(strict_undefined=False)
    x = JinjaService(config, context_service)
    assert x.render_string("foo{{ bar }}") == "foo"
