import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

from dataclasses_json import DataClassJsonMixin, Undefined
from dotenv import dotenv_values

from jinja_tree.app.config import Config
from jinja_tree.app.context import ContextPort
from jinja_tree.infra.utils import is_fnmatch_ignored

ENV_CONTEXT_ADAPTER_DEFAULT_IGNORES: List[str] = []
DOTENV_CONTEXT_ADAPTER_DEFAULT_PATH = ".env"
DOTENV_CONTEXT_ADAPTER_DEFAULT_IGNORES: List[str] = []


@dataclass
class EnvContextConfig(DataClassJsonMixin):
    ignores: List[str] = field(
        default_factory=lambda: list(ENV_CONTEXT_ADAPTER_DEFAULT_IGNORES)
    )
    dataclass_json_config = {"undefined": Undefined.RAISE}  # noqa: RUF012


class EnvContextAdapter(ContextPort):
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        self.config = config
        self.plugin_config = EnvContextConfig.from_dict(plugin_config)

    @classmethod
    def get_config_name(cls) -> str:
        return "env"

    def get_context(self) -> Dict[str, Any]:
        if self.plugin_config.ignores == ["*"]:
            return {}
        return {
            x: y
            for x, y in os.environ.items()
            if not is_fnmatch_ignored(x, self.plugin_config.ignores)
        }


@dataclass
class DotEnvContextConfig(DataClassJsonMixin):
    path: str = DOTENV_CONTEXT_ADAPTER_DEFAULT_PATH
    ignores: List[str] = field(
        default_factory=lambda: list(DOTENV_CONTEXT_ADAPTER_DEFAULT_IGNORES)
    )
    dataclass_json_config = {"undefined": Undefined.RAISE}  # noqa: RUF012

    def __post_init__(self):
        self.path = os.path.abspath(self.path)


class DotEnvContextAdapter(ContextPort):
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        self.config = config
        self.plugin_config = DotEnvContextConfig.from_dict(plugin_config)

    @classmethod
    def get_config_name(cls) -> str:
        return "dotenv"

    def get_context(self) -> Dict[str, Any]:
        if not self.plugin_config.path:
            return {}
        if not os.path.isfile(self.plugin_config.path):
            return {}
        if self.plugin_config.ignores == ["*"]:
            return {}
        return {
            x: y
            for x, y in dotenv_values(self.plugin_config.path).items()
            if not is_fnmatch_ignored(x, self.plugin_config.ignores)
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
