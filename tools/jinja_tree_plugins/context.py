import inspect
from typing import Any, Dict

from jinja_tree.app.action import (
    CONCRETE_DIRECTORY_ACTIONS,
    CONCRETE_FILE_ACTIONS,
    ActionPort,
)
from jinja_tree.app.config import EMBEDDED_EXTENSIONS, Config
from jinja_tree.app.context import ContextPort
from jinja_tree.infra.adapters.action import (
    DEFAULT_EXTENSIONS,
    DELETE_ORIGINAL_DEFAULT,
    DIRNAME_IGNORES_DEFAULT,
    FILENAME_IGNORES_DEFAULT,
    REPLACE_DEFAULT,
)
from jinja_tree.infra.adapters.context import (
    DOTENV_CONTEXT_ADAPTER_DEFAULT_IGNORES,
    DOTENV_CONTEXT_ADAPTER_DEFAULT_PATH,
    ENV_CONTEXT_ADAPTER_DEFAULT_IGNORES,
)


class CustomEnvContextAdapter(ContextPort):
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        self.config = config
        self.plugin_config = plugin_config

    @classmethod
    def get_config_name(cls) -> str:
        return "custom_env"

    def get_context(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        res["default_config"] = Config()
        res["dirname_ignores_default"] = DIRNAME_IGNORES_DEFAULT
        res["filename_ignores_default"] = FILENAME_IGNORES_DEFAULT
        res["embedded_jinja_extensions"] = EMBEDDED_EXTENSIONS
        res["context_port_source"] = inspect.getsource(ContextPort)
        res["action_port_source"] = inspect.getsource(ActionPort)
        res["file_actions_source"] = "\n\n".join(
            inspect.getsource(action) for action in CONCRETE_FILE_ACTIONS
        )
        res["directory_actions_source"] = "\n\n".join(
            inspect.getsource(action) for action in CONCRETE_DIRECTORY_ACTIONS
        )
        res["ENV_CONTEXT_ADAPTER_DEFAULT_IGNORES"] = ENV_CONTEXT_ADAPTER_DEFAULT_IGNORES
        res["DOTENV_CONTEXT_ADAPTER_DEFAULT_PATH"] = DOTENV_CONTEXT_ADAPTER_DEFAULT_PATH
        res[
            "DOTENV_CONTEXT_ADAPTER_DEFAULT_IGNORES"
        ] = DOTENV_CONTEXT_ADAPTER_DEFAULT_IGNORES
        res["DEFAULT_EXTENSIONS"] = DEFAULT_EXTENSIONS
        res["REPLACE_DEFAULT"] = REPLACE_DEFAULT
        res["DELETE_ORIGINAL_DEFAULT"] = DELETE_ORIGINAL_DEFAULT
        res["DIRNAME_IGNORES_DEFAULT"] = DIRNAME_IGNORES_DEFAULT
        res["FILENAME_IGNORES_DEFAULT"] = FILENAME_IGNORES_DEFAULT
        return res
