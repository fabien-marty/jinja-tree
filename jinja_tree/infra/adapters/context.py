import os
from typing import Any, Dict, List, cast

from dotenv import dotenv_values

from jinja_tree.app.config import Config
from jinja_tree.app.context import ContextPort
from jinja_tree.infra.utils import is_fnmatch_ignored

ENV_CONTEXT_ADAPTER_DEFAULT_IGNORES: List[str] = []
DOTENV_CONTEXT_ADAPTER_DEFAULT_PATH = ".env"
DOTENV_CONTEXT_ADAPTER_DEFAULT_IGNORES: List[str] = []


class EnvContextAdapter(ContextPort):
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        self.config = config
        self.plugin_config = plugin_config
        self.ignores = cast(
            List[str],
            self.plugin_config.get("ignores", ENV_CONTEXT_ADAPTER_DEFAULT_IGNORES),
        )

    @classmethod
    def get_config_name(cls) -> str:
        return "env"

    def get_context(self) -> Dict[str, Any]:
        if self.ignores == ["*"]:
            return {}
        return {
            x: y
            for x, y in os.environ.items()
            if not is_fnmatch_ignored(x, self.ignores)
        }


class DotEnvContextAdapter(ContextPort):
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        self.config = config
        self.plugin_config = plugin_config
        self.path = self.plugin_config.get("path", DOTENV_CONTEXT_ADAPTER_DEFAULT_PATH)
        self.ignores = cast(
            List[str],
            self.plugin_config.get("ignores", DOTENV_CONTEXT_ADAPTER_DEFAULT_IGNORES),
        )

    @classmethod
    def get_config_name(cls) -> str:
        return "dotenv"

    def get_context(self) -> Dict[str, Any]:
        if not self.path:
            return {}
        if not os.path.isfile(self.path):
            return {}
        if self.ignores == ["*"]:
            return {}
        return {
            x: y
            for x, y in dotenv_values(self.path).items()
            if not is_fnmatch_ignored(x, self.ignores)
        }


class ConfigurationContextAdapter(ContextPort):
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        self.config = config
        self.plugin_config = plugin_config

    @classmethod
    def get_config_name(cls) -> str:
        return "config"

    def get_context(self) -> Dict[str, Any]:
        return self.plugin_config
