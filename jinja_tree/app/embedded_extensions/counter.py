from jinja2.ext import Extension


def counter(environment, start=None, name="default"):
    counters = getattr(environment, "_counter_values", None)
    if counters is None:
        counters = {}
        environment._counter_values = counters

    if name not in counters:
        counters[name] = 0 if start is None else start

    current_value = counters[name]
    counters[name] += 1
    return current_value


class CounterExtension(Extension):
    """Jinja2 extension to expose incrementing named counters.

    Examples:
    {{ counter() }} {{ counter() }}
    => 0 1

    {{ counter(name='foo', start=3) }} {{ counter(name='foo') }}
    => 3 4
    """

    def __init__(self, environment):
        super().__init__(environment)
        environment.globals["counter"] = lambda start=None, name="default": counter(
            environment, start=start, name=name
        )
