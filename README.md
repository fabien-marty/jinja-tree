<!-- *** GENERATED FILE - DO NOT EDIT *** -->
<!-- To modify this file, edit README.md.template and launch 'make doc' -->

# jinja-tree

![Python Badge](https://raw.githubusercontent.com/fabien-marty/common/refs/heads/main/badges/python38plus.svg)
[![UV Badge](https://raw.githubusercontent.com/fabien-marty/common/refs/heads/main/badges/uv.svg)](https://docs.astral.sh/uv/)
[![Task Badge](https://raw.githubusercontent.com/fabien-marty/common/refs/heads/main/badges/task.svg)](https://taskfile.dev/)
[![Mergify Badge](https://raw.githubusercontent.com/fabien-marty/common/refs/heads/main/badges/mergify.svg)](https://mergify.com/)
[![Renovate Badge](https://raw.githubusercontent.com/fabien-marty/common/refs/heads/main/badges/renovate.svg)](https://docs.renovatebot.com/)
[![MIT Licensed](https://raw.githubusercontent.com/fabien-marty/common/refs/heads/main/badges/mit.svg)](https://en.wikipedia.org/wiki/MIT_License)

## What is it?

`jinja-tree` is a CLI utility to process [jinja (jinja2)](https://jinja.palletsprojects.com/) templates
recursively in a directory tree.

It is very configurable and very easy to extend with its included plugin system.

The default behavior is to recursively search for files with a given extension (`.template` for example) and to process the context with [Jinja (Jinja2)](https://jinja.palletsprojects.com/) templates engine reading the context variables from:

- a configuration file
- environment variables 
- dotenv files 

Then, the processed content is written into another file with the same name/path but with the configured extension (`.template` by default) removed. The original file can also be deleted (but this is not the default behavior).

<details>

<summary>Full example about overall operation (in default mode)</summary>

Note: this is only the **default behavior** as you can tune this with your own plugins!

Let's imagine the following directory structure:

```
/foo/
/foo/README.md.template
/foo/bar/baz.py.template
/foo/bar/another.file
```

And execute `jinja-tree /foo` with the default configuration.

We get:

```
/foo/
/foo/README.md.template
/foo/README.md <= NEW FILE FROM README.md.template jinja2 processing
/foo/bar/baz.py.template
/foo/bar/baz.py <= NEW FILE FROM baz.py.template jinja2 processing 
/foo/bar/another.file
```

</details>

## What's it for?

Your imagination is your limit 😅 but it's very useful for maintaining DRY documentation (for example `your-cli --help` output automatically updated in a markdown file), configuration files with default values read in code, including common blocks in different files...

**So it's a great tool for maintaining repositories in general.**

> [!TIP]
> Do you cant real-life examples? You can find some details about how we use it in this repository for:
> 
> - [getting `jinja-tree --help` output automatically added (and updated) in this README](docs/details-about-real-life-example1.md)
> - [getting a reference TOML configuration file rendered with default values read from code](docs/details-about-real-life-example2.md)

> [!NOTE]
> Another "action" plugin will be soon 🕒 provided to bootstrap directory trees from templates (like with the [cookiecutter](https://github.com/cookiecutter/cookiecutter) project).

## Features

#### 1️⃣ Easy to extend 

`jinja-tree` includes a plugin system. You can override the default behavior with your own plugins.

There are two extension points:

- context plugins: to provide context variables to Jinja templates
- file plugins: to change the way how `jinja-tree` finds files to process (including target files)

See [this specification documentation page](docs/details-about-plugins.md) for more details.

#### 2️⃣ Very configurable

`jinja-tree` is very configurable. You can configure global options via CLI options or a configuration file. 

Plugins are configurable via the configuration file.

See [this specification documentation page](docs/details-about-configuration.md) for more details.

#### 3️⃣ Embedded extensions

`jinja-tree` includes some extensions to Jinja templates engine:

- [to execute some commands (and get the corresponding output)](jinja_tree/app/embedded_extensions/shell.py)
- [to parse JSON strings into Python objects)](jinja_tree/app/embedded_extensions/from_json.py)
- ..

<details>

<summary>Usage examples</summary>

#### `shell` extension


```jinja
{{ "date"|shell() }}
```

=> will render something like: `Sun Jan 28 15:11:44 CET 2024`


#### `from_json` extension


```bash
export MYENV='["foo", "bar", "baz"]'

(
    cat <<EOF
{% for item in MYENV|from_json() -%}
- {{ item }}
{% endfor %}
EOF
) | jinja-stdin
```


=> will render something like:

```
- foo
- bar
- bar
```

</details>

See [this directory](jinja_tree/app/embedded_extensions/) for others

#### 4️⃣ Full Jinja / Jinja2 support (including "includes" and "inheritance")

`jinja-tree` has several options for Jinja "search paths". So you can use Jinja "includes" and "inheritance" features.

## Installation

`pip install jinja-tree`

> [!TIP]
> If you want to get a better readability of `jinja-tree` output (colors...), you can also use `pip install rich` to install 
> this **optional** dependency.

> [!NOTE]
> A docker image is also available. You can use it to avoid any specific installation.
> See at the end of the "Usage" section for more details.

## Usage

### Main CLI

```
jinja-tree .
```

> [!NOTE]
> The `.` in the previous command in the "root directory" (the directory `jinja-tree` will explore recursively to find files to process). You can replace it with any directory you want. By using `.`, you will process all files in the current directory and its subdirectories.

<details>

<summary>Main CLI options</summary>

```
Usage: jinja-tree [OPTIONS] ROOT_DIR

  Process a directory tree with the Jinja / Jinja2 templating system.

Arguments:
  ROOT_DIR  root directory  [required]

Options:
  --config-file TEXT              config file path (default: first '.jinja-
                                  tree.toml' file found up from current
                                  working dir), can also be see with
                                  JINJA_TREE_CONFIG_FILE env var  [env var:
                                  JINJA_TREE_CONFIG_FILE]
  --log-level TEXT                log level (DEBUG, INFO, WARNING or ERROR)
                                  [default: INFO]
  --verbose / --no-verbose        increase verbosity of the DEBUG log level
                                  (note: this forces log-level = DEBUG)
                                  [default: no-verbose]
  --extra-search-path PATH        Search path to jinja (can be used multiple
                                  times)
  --add-cwd-to-search-path / --no-add-cwd-to-search-path
                                  add current working directory (CWD) to jinja
                                  search path
  --add-root-dir-to-search-path / --no-add-root-dir-to-search-path
                                  add root directory to jinja search path
  --jinja-extension TEXT          jinja extension to load
  --context-plugin TEXT           context plugins (full python class path, can
                                  be used multiple times)
  --action-plugin TEXT            action plugin (full python class path, can
                                  be used multiple times)
  --strict-undefined / --no-strict-undefined
                                  if set, raise an error if a variable does
                                  not exist in context
  --blank-run / --no-blank-run    if set, execute a blank run (without
                                  modifying or deleting anything)  [default:
                                  no-blank-run]
  --disable-embedded-jinja-extensions / --no-disable-embedded-jinja-extensions
                                  disable embedded jinja extensions
  --help                          Show this message and exit.

``` 

</details>

### Bonus CLI (if you want to process only one file but with the same behavior)

```bash
cat /path/to/your/file/to/process | jinja-stdin >/path/to/your/processed/file
```

or (if you want to process only a string):


```console
$ export FOO=bar
$ echo "Hello {{FOO}}" | jinja-stdin
Hello bar
```


<details>

<summary>Bonus CLI options</summary>

```
Usage: jinja-stdin [OPTIONS]

  Process the standard input with Jinja templating system and return the
  result on the standard output.

Options:
  --config-file TEXT              config file path (default: first '.jinja-
                                  tree.toml' file found up from current
                                  working dir), can also be see with
                                  JINJA_TREE_CONFIG_FILE env var  [env var:
                                  JINJA_TREE_CONFIG_FILE]
  --log-level TEXT                log level (DEBUG, INFO, WARNING or ERROR)
                                  [default: INFO]
  --verbose / --no-verbose        increase verbosity of the DEBUG log level
                                  (note: this forces log-level = DEBUG)
                                  [default: no-verbose]
  --extra-search-path PATH        Search path to jinja (can be used multiple
                                  times)
  --add-cwd-to-search-path / --no-add-cwd-to-search-path
                                  add current working directory (CWD) to jinja
                                  search path
  --jinja-extension TEXT          jinja extension to load
  --context-plugin TEXT           context plugins (full python class path, can
                                  be used multiple times)
  --strict-undefined / --no-strict-undefined
                                  if set, raise an error if a variable does
                                  not exist in context
  --disable-embedded-jinja-extensions / --no-disable-embedded-jinja-extensions
                                  disable embedded jinja extensions
  --help                          Show this message and exit.

``` 

</details>

### Docker image

A docker image is also available. You can use it this way:

```bash
docker run --rm -t -v $(pwd):/code --user=$(id -u) ghcr.io/fabien-marty/jinja-tree:latest /code
```

*(we mount the current directory in the `/code` directory in the container and execute `jinja-tree` in this `/code` directory)*

> [!WARNING]
> If you plan to use environment variables with the docker image, you will have to use (possibly multiple times) the `-e VAR=VALUE` option to pass them to the container. 
> With docker, it's more practical to use a `.env` (dotenv) file as it will be automatically mounted in the container.

If you want to add some CLI options, you can add them like in this example:

```bash
docker run --rm -t -v $(pwd):/code --user=$(id -u) ghcr.io/fabien-marty/jinja-tree:latest --verbose /code
```

*(we added `--verbose` just before the `/code` argument)*

<details>

<summary>If you want to use the `jinja-stdin` CLI with docker?</summary>


```bash
echo "FOO {{ BAR }}" |docker run --rm -i -e BAR=BAZ --user=$(id -u) --entrypoint /app/entrypoint-stdin.sh ghcr.io/fabien-marty/jinja-tree:latest
```


*(it will output `FOO BAZ`)*

</details>