import json

from jinja2 import pass_eval_context as eval_context
from jinja2.ext import Extension


@eval_context
def from_json(eval_ctx, value):
    return json.loads(value)


class FromJsonExtension(Extension):
    """Jinja2 extension to load a JSON string into a Python object."""

    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["from_json"] = from_json
