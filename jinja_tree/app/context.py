import datetime
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from jinja2 import Template

from jinja_tree.app import dump
from jinja_tree.app.config import Config


class ContextPort(ABC):
    """This is the abstract interface for ContextPort adapters."""

    @abstractmethod
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        """
        Construct a new ContextPort object given a configuration object
        and a plugin configuration dict.

        Args:
            config (Config): The configuration object.
            plugin_config (Dict[str, Any]): The plugin configuration dict.

        """
        pass

    @abstractmethod
    def get_context(self) -> Dict[str, Any]:
        """
        Retrieve the Jinja context to apply.

        Note: it can depends on the current working directory (CWD).

        Returns:
            The context dictionary.

        """
        pass

    @classmethod
    @abstractmethod
    def get_config_name(cls) -> str:
        """
        Return the name of the configuration object.

        For example, if we return "foo", it means that the configuration in the TOML file
        is located under:

        [context.foo]
        # ... some configuration ...

        Returns:
            The name of the configuration object.

        """
        pass


def make_generated_comment(
    template_string: str,
    utcnow: str,
    absolute_path: str,
    dirname: str,
    basename: str,
    relative_filepath: str,
) -> str:
    return Template(source=template_string).render(
        utcnow=utcnow,
        absolute_path=absolute_path,
        dirname=dirname,
        basename=basename,
        relative_filepath=relative_filepath,
    )


class ContextService:
    """This service is responsible for retrieving the Jinja context to apply.

    It's a kind of proxy object on ContextPort adapters to factorize some common logic.

    Attributes:
        config: The configuration object.
        adapters: The ContextPort adapters to use.

    """

    def __init__(self, config: Config, adapters: List[ContextPort]):
        self.config = config
        self.adapters = adapters
        self.comment_line1_template = self.config.context_generated_comment_line1
        self.comment_line2_template = self.config.context_generated_comment_line2
        if self.config.verbose:
            dump("initial context", self.get_context())

    def add_extra_keys_to_context(
        self, context: Dict[str, Any], absolute_path: Optional[str] = None
    ):
        context["JINJA_TREE"] = "1"
        try:
            utcnow = datetime.datetime.now(datetime.UTC).isoformat()[0:19] + "Z"  # type: ignore
        except AttributeError:
            # for python <= 3.10
            utcnow = datetime.datetime.utcnow().isoformat()[0:19] + "Z"  # type: ignore

        context["JINJA_DT"] = utcnow
        if absolute_path:
            context["JINJA_TREE_FILEPATH"] = absolute_path
            dirname = os.path.dirname(absolute_path)
            context["JINJA_TREE_DIRNAME"] = dirname
            basename = os.path.basename(absolute_path)
            context["JINJA_TREE_BASENAME"] = basename
            context["JINJA_TREE_ROOT_DIR"] = self.config.root_dir
            if absolute_path.startswith(self.config.root_dir):
                # should be true...
                relative_filepath = absolute_path[len(self.config.root_dir) + 1 :]
                context["JINJA_TREE_RELATIVE_FILEPATH"] = relative_filepath
                make_generated_comment_kwargs = {
                    "utcnow": utcnow,
                    "absolute_path": absolute_path,
                    "dirname": dirname,
                    "basename": basename,
                    "relative_filepath": relative_filepath,
                }
                comment_line1 = make_generated_comment(
                    self.comment_line1_template, **make_generated_comment_kwargs
                )
                comment_line2 = make_generated_comment(
                    self.comment_line2_template, **make_generated_comment_kwargs
                )
                context["JINJA_TREE_STYLE1_GENERATED_COMMENT"] = "\n".join(
                    [f"<!-- {x} -->" for x in (comment_line1, comment_line2) if x]
                )
                context["JINJA_TREE_STYLE2_GENERATED_COMMENT"] = "\n".join(
                    [f"# {x}" for x in (comment_line1, comment_line2) if x]
                )
                context["JINJA_TREE_STYLE3_GENERATED_COMMENT"] = "\n".join(
                    [f"// {x}" for x in (comment_line1, comment_line2) if x]
                )

    def get_context(self, absolute_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve the Jinja context to apply.

        Note: it can depends on the current working directory (CWD).

        Returns:
            The context dictionary.

        """
        res: Dict[str, Any] = {}
        for adapter in self.adapters:
            res = {**res, **adapter.get_context()}
        self.add_extra_keys_to_context(res, absolute_path=absolute_path)
        return res
