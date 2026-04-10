import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

import tomli
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


@dataclass
class TOMLContextConfig(DataClassJsonMixin):
    paths: List[str] = field(
        default_factory=lambda: [
            x.strip()
            for x in os.environ.get("JINJA_TREE_TOML_CONTEXT_PATHS", "").split(",")
            if x.strip()
        ]
    )
    path: str = field(
        default_factory=lambda: os.environ.get("JINJA_TREE_TOML_CONTEXT_PATH", "")
    )  # deprecated, use paths instead (kept for backward compatibility)
    dataclass_json_config = {"undefined": Undefined.RAISE}  # noqa: RUF012

    def __post_init__(self):
        if not self.paths and self.path:
            # backward compatibility with old config files using singular "path"
            self.paths = [self.path]
        self.paths = [os.path.abspath(x) for x in self.paths]


class TOMLContextAdapter(ContextPort):
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        self.config = config
        self.plugin_config = TOMLContextConfig.from_dict(plugin_config)

    @classmethod
    def get_config_name(cls) -> str:
        return "toml"

    def _get_context_single_path(self, path: str) -> Dict[str, Any]:
        try:
            with open(path) as f:
                content = f.read()
        except Exception:
            raise Exception(f"Failed to read {path}")
        try:
            return tomli.loads(content)
        except Exception:
            raise Exception(f"Failed to parse {path}")

    def get_context(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        for path in self.plugin_config.paths:
            if path:
                res.update(self._get_context_single_path(path))
        return res
