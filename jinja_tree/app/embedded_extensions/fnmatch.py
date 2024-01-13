import fnmatch

from jinja2 import pass_eval_context as eval_context
from jinja2.ext import Extension


@eval_context
def _fnmatch(eval_ctx, value, pattern):
    return fnmatch.fnmatch(value, pattern)


class FnMatchExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["fnmatch"] = _fnmatch
