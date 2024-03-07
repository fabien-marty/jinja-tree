import tomli
from jinja2 import pass_eval_context as eval_context
from jinja2.ext import Extension


@eval_context
def from_toml(eval_ctx, value):
    return tomli.loads(value)


class FromTomlExtension(Extension):
    """Jinja2 extension to load a TOML string into a Python object."""

    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["from_toml"] = from_toml
