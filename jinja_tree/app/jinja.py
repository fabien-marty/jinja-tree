import os
from typing import Optional

import stlog
from jinja2 import (
    ChoiceLoader,
    DictLoader,
    Environment,
    FileSystemLoader,
    StrictUndefined,
    Undefined,
    UndefinedError,
)

from jinja_tree.app.config import Config
from jinja_tree.app.context import ContextService

logger = stlog.getLogger("jinja-tree")


class JinjaService:
    """Service to render a string with Jinja2 calling the context service to get the context."""

    def __init__(
        self,
        config: Config,
        context_service: ContextService,
    ):
        self.context_service = context_service
        self.template_name = "__content"
        self.config = config

    def render_string(self, content: str, absolute_path: Optional[str] = None) -> str:
        """
        Renders the given content as a Jinja template string.

        The context is retrieved from the ContextService.

        Args:
            content: The content to render as a template.
            absolute_path: The absolute path of the template file (if available).

        Returns:
            str: The rendered output as a string.
        """
        loader1 = DictLoader({self.template_name: content})
        paths = []
        if self.config.add_root_dir_to_search_path:
            paths.append(self.config.root_dir)
        if self.config.add_processed_file_dir_to_search_path:
            paths.append(os.getcwd())
        if self.config.extra_search_paths:
            paths = paths + [str(x) for x in self.config.extra_search_paths]
        loader2 = FileSystemLoader(paths, followlinks=True)
        loader = ChoiceLoader([loader1, loader2])
        env = Environment(
            loader=loader,
            undefined=StrictUndefined if self.config.strict_undefined else Undefined,
            extensions=self.config.resolved_extensions,
        )
        template = env.get_template(self.template_name)
        template.globals = self.context_service.get_context(absolute_path)
        self.context_service.get_context()
        try:
            output = template.render()
        except UndefinedError:
            logger.error(
                "error during the template rendering because of undefined variables (you can use the --no-strict-undefined flag to disable this)",
                path=absolute_path,
            )
            raise
        return output
