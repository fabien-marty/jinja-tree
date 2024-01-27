from jinja2 import pass_eval_context as eval_context
from jinja2.ext import Extension


@eval_context
def double_quotes(eval_ctx, value):
    return '"' + value + '"'


class DoubleQuotesExtension(Extension):
    """Jinja2 extension to add double quotes around a string.

    Example:
    {{ 'foo-bar'|double_quotes() }}

    => "foo-bar"

    """

    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["double_quotes"] = double_quotes
