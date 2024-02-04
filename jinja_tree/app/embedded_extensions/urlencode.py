from urllib.parse import quote

from jinja2 import pass_eval_context as eval_context
from jinja2.ext import Extension


@eval_context
def urlencode_filter(eval_ctx, value, safe="/"):
    return quote(value, safe=safe)


class UrlEncodeExtension(Extension):
    """Jinja2 extension to urlencode a string.

    Example:
    {{ 'https://google.com'|urlencode(safe='') }}

    => "https%3A%2F%2Fgoogle.com"

    """

    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["urlencode"] = urlencode_filter
