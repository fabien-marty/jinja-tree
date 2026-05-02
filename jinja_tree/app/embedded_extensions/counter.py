from jinja2.ext import Extension


def get_named_values(environment):
    named_values = getattr(environment, "_counter_named_values", None)
    if named_values is None:
        named_values = {}
        environment._counter_named_values = named_values
    return named_values


def counter(environment, start=None, name="default", set_value_name=None):
    counters = getattr(environment, "_counter_values", None)
    if counters is None:
        counters = {}
        environment._counter_values = counters

    named_values = get_named_values(environment)
    if set_value_name is not None and set_value_name in named_values:
        raise ValueError(f"counter value name '{set_value_name}' is already defined")

    if name not in counters:
        counters[name] = 1 if start is None else start

    current_value = counters[name]
    counters[name] += 1

    if set_value_name is not None:
        named_values[set_value_name] = current_value

    return current_value


def counter_value(environment, name):
    named_values = get_named_values(environment)
    if name not in named_values:
        raise ValueError(f"counter value name '{name}' is not defined")
    return named_values[name]


class CounterExtension(Extension):
    """Jinja2 extension to expose incrementing named counters.

    Examples:
    {{ counter() }} {{ counter() }}
    => 1 2

    {{ counter(name='foo', start=3) }} {{ counter(name='foo') }}
    => 3 4

    {{ counter(name='steps', set_value_name='login') }} {{ counter_value('login') }}
    => 1 1
    """

    def __init__(self, environment):
        super().__init__(environment)
        environment.globals["counter"] = (
            lambda start=None, name="default", set_value_name=None: counter(
                environment,
                start=start,
                name=name,
                set_value_name=set_value_name,
            )
        )
        environment.globals["counter_value"] = lambda name: counter_value(
            environment, name
        )
