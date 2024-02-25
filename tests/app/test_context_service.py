from typing import Any, Dict, Optional

from jinja_tree.app.config import Config
from jinja_tree.app.context import ContextPort, ContextService


class MockContextAdapter(ContextPort):
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        pass

    @classmethod
    def get_config_name(cls) -> str:
        return "mock"

    def get_context(self, absolute_path: Optional[str] = None) -> Dict[str, Any]:
        return {"foo": "bar"}


def test_context_service():
    config = Config()
    context_adapter = MockContextAdapter(config, {})
    x = ContextService(config, [context_adapter])
    res = x.get_context()
    assert res["foo"] == "bar"
    assert res["JINJA_TREE"] == "1"
    res = x.get_context("/foo/bar.template")
    assert len(res) > 4
