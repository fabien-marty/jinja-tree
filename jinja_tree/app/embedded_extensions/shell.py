import subprocess

from jinja2 import pass_eval_context as eval_context
from jinja2.ext import Extension


@eval_context
def shell(eval_ctx, value, die_on_error=True, encoding="utf8", **kwargs):
    if die_on_error:
        cmd = value
    else:
        cmd = "%s ; exit 0" % value
    return subprocess.check_output(
        cmd, stderr=subprocess.STDOUT, shell=True, encoding=encoding, **kwargs
    )


class ShellExtension(Extension):
    """Jinja2 extension to execute shell commands.

    Example:
    {{ "date"|shell() }}

    => "Thu  7 Nov 2019 15:55:01 CET"

    WARNING: be sure to valid any string submitted to this filter as
             you can open security holes with it

    """

    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["shell"] = shell
