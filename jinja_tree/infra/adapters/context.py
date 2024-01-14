import os
from typing import Any, Dict, List, cast

from dotenv import dotenv_values

from jinja_tree.app.config import Config
from jinja_tree.app.context import ContextPort
from jinja_tree.infra.utils import is_fnmatch_ignored


class EnvContextAdapter(ContextPort):
    def __init__(self, config: Config):
        self.env_ignores = cast(
            List[str], config.context_plugin_config.get("env_ignores")
        )
        assert self.env_ignores is not None
        self.plugin_configuration_ignores = cast(
            List[str], config.context_plugin_config.get("plugin_configuration_ignores")
        )
        assert self.plugin_configuration_ignores is not None
        self.dotenv_path = config.context_plugin_config.get("dotenv_path")
        assert self.dotenv_path is not None
        self.dotenv_ignores = cast(
            List[str], config.context_plugin_config.get("dotenv_ignores")
        )
        assert self.dotenv_ignores is not None
        self.config = config

    def get_plugin_configuration_context(self) -> Dict[str, Any]:
        if self.plugin_configuration_ignores == ["*"]:
            return {}
        return {
            x: y
            for x, y in self.config.context_plugin_config.items()
            if not is_fnmatch_ignored(x, self.plugin_configuration_ignores)
        }

    def get_dotenv_context(self) -> Dict[str, Any]:
        if not self.dotenv_path:
            return {}
        if not os.path.isfile(self.dotenv_path):
            return {}
        if self.dotenv_ignores == ["*"]:
            return {}
        return {
            x: y
            for x, y in dotenv_values(self.dotenv_path).items()
            if not is_fnmatch_ignored(x, self.dotenv_ignores)
        }

    def get_env_context(self) -> Dict[str, Any]:
        if self.env_ignores == ["*"]:
            return {}
        return {
            x: y
            for x, y in os.environ.items()
            if not is_fnmatch_ignored(x, self.env_ignores)
        }

    def get_context(self) -> Dict[str, Any]:
        plugin_context = self.get_plugin_configuration_context()
        env_context = self.get_env_context()
        dotenv_context = self.get_dotenv_context()
        return {**plugin_context, **env_context, **dotenv_context}
