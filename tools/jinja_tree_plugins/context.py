import inspect
from typing import Any, Dict

from jinja_tree.app.action import (
    CONCRETE_DIRECTORY_ACTIONS,
    CONCRETE_FILE_ACTIONS,
    ActionPort,
)
from jinja_tree.app.config import (
    DIRNAME_IGNORES_DEFAULT,
    EMBEDDED_EXTENSIONS,
    FILENAME_IGNORES_DEFAULT,
    Config,
)
from jinja_tree.app.context import ContextPort
from jinja_tree.infra.adapters.context import EnvContextAdapter


class CustomEnvContextAdapter(EnvContextAdapter):
    def get_context(self) -> Dict[str, Any]:
        tmp = super().get_context()
        tmp["default_config"] = Config()
        tmp["dirname_ignores_default"] = DIRNAME_IGNORES_DEFAULT
        tmp["filename_ignores_default"] = FILENAME_IGNORES_DEFAULT
        tmp["embedded_jinja_extensions"] = EMBEDDED_EXTENSIONS
        tmp["context_port_source"] = inspect.getsource(ContextPort)
        tmp["action_port_source"] = inspect.getsource(ActionPort)
        tmp["file_actions_source"] = "\n\n".join(
            inspect.getsource(action) for action in CONCRETE_FILE_ACTIONS
        )

        tmp["directory_actions_source"] = "\n\n".join(
            inspect.getsource(action) for action in CONCRETE_DIRECTORY_ACTIONS
        )

        return tmp
