# Getting a reference TOML configuration file rendered with default values read from code

> [!TIP]
> Read [this first example](details-about-real-life-example1.md) first.

## How it works

This use case is a little more complicated. We have to maintain [this file: `jinja-tree.toml`](jinja-tree.toml) as a reference default configuration file but 
we don't want to duplicate default values from the code in this file (DRY principle).

Like with [the first example](details-about-real-life-example1.md), we use `jinja-tree` to render the [`jinja-tree.toml`](jinja-tree.toml) file from a [`jinja-tree.toml.template`](jinja-tree.toml.template) file.

But this time, to inject default values from the code as context variables for the Jinja2 processing, we have to write a [custom plugin](details-about-plugins.md).

The full code of this "context plugin" is in the file [`tools/jinja_tree_plugins/context.py`](../tools/jinja_tree_plugins/context.py) but a simplified version could be:

```python
from typing import Any, Dict
from jinja_tree.app.config import (
    EMBEDDED_EXTENSIONS,
    DIRNAMES_IGNORES_DEFAULT,
    Config,
)
from jinja_tree.app.context import ContextPort
from jinja_tree.infra.adapters.action import DIRNAME_IGNORES_DEFAULT

class CustomEnvContextAdapter(ContextPort):

    @classmethod
    def get_config_name(cls) -> str:
        return "custom_env"

    def get_context(self) -> Dict[str, Any]:
        tmp = super().get_context() # we override the default behavior
        tmp["default_config"] = Config() # we publish the default configuration as a "default_config" context variable
        tmp["dirname_ignores_default"] = DIRNAME_IGNORES_DEFAULT # we publish other default values
        tmp["embedded_jinja_extensions"] = EMBEDDED_EXTENSIONS # ...
        return tmp
```

Then we have to activate our plugin with `--context-plugin` CLI option (or in the `context_plugins` key of the configuration file).

Now in the `jinja-tree.toml.template` file, we can use these context variables. For examples:

```toml
# Change working directory when tree walking (if true)
change_cwd = {{ default_config.change_cwd|lower }}
```

to get: `change_cwd = true` in the target file.

More complex example:

```toml
[action.extension]

# Dirname patterns to ignore recursively (fnmatch patterns to match against dirname only)
ignores =  [ {{ dirname_ignores_default|map('double_quotes')|join(', ') }} ]
```

to get: `dirname_ignores =  [ "venv", "site-packages", "__pypackages__", "node_modules", "__pycache__", ".*" ]` in the target file.

Of course, you can also use loops:

```toml
# Disable embedded jinja extensions (if true)
# List of embedded jinja extensions (for information only):
{% for x in embedded_jinja_extensions -%}
# - {{x}}
{% endfor -%}
```

to get:

```toml
# Disable embedded jinja extensions (if true)
# List of embedded jinja extensions (for information only):
# - jinja_tree.app.embedded_extensions.from_json.FromJsonExtension
# - jinja_tree.app.embedded_extensions.shell.ShellExtension
# - jinja_tree.app.embedded_extensions.fnmatch.FnMatchExtension
# - jinja_tree.app.embedded_extensions.double_quotes.DoubleQuotesExtension
# - jinja_tree.app.embedded_extensions.urlencode.UrlEncodeExtension
```

## Bonus

If you have a look at the real [context plugin](../tools/jinja_tree_plugins/context.py), you will find lines like:

```python
tmp["context_port_source"] = inspect.getsource(ContextPort)
```

So we can easily publish the source code of a class or a function without including the whole file. This can be very useful for documentation.
In this repository, it's used in the [plugin documentation](details-about-plugins.md).

Go back to [main README](../README.md) file.