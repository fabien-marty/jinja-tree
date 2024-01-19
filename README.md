<!-- *** GENERATED FILE - DO NOT EDIT *** -->
<!-- To modify this file, edit README.md.template and launch 'make doc' -->

# jinja-tree

## What is it?

`jinja-tree` is a CLI utility to process [jinja (jinja2)](https://jinja.palletsprojects.com/) templates
recursively in a directory tree.

It is very configurable and very easy to extend with its included plugin system.

The default behavior is to recursively search for files with a given extension (`.template` for example) and to process the context with [jinja (jinja2)](https://jinja.palletsprojects.com/) templates engine reading the context variables from:

- a configuration file
- environment variables 
- dotenv files 

Then, the processed content is written into another file with the same name/path but with the configured extension (`.template` by default) removed. The original file can also be deleted (but this is not the default behavior).

> [!TIP]
> If you want a full example about overall operation, you can find an [example here](docs/details-about-overall-operation.md).

## What's it for?

Your imagination is your limit 😅 but it's very useful for maintaining DRY documentation (for example: `your-cli --help` output automatically updated in a markdown file), configuration files with default values read in code, included common blocks in different files...

**So it's a great tool for maintaining repositories in general.**

> [!TIP]
> Do you cant real-life examples? You can find some details about how we use it in this repository for:
> 
> - [getting `jinja-tree --help` output automatically added (and updated) in this README](docs/fixme)
> - [getting a reference TOML configuration file rendered with defaults values read from code](docs/fixme)

## Features

#### 1️⃣ Easy to extend 

`jinja-tree` includes a plugin system. You can override the default behavior with your own plugins.

There is two extension points:

- context plugins: to provide context variables to jinja templates
- file plugins: to change the way how `jinja-tree` find files to process (including target files)

See [this specification documentation page](docs/fixme) for more details.

#### 2️⃣ Very configurable

#### 3️⃣ Embedded extensions

#### 4️⃣ Full Jinja / Jinja2 support (including "includes" and "inheritance")

## Installation

`pip install jinja-tree`

A docker image will also be available soon 🕒

## CLI options

```
$ jinja-tree --help 
Usage: cli_tree.py [OPTIONS] ROOT_DIR

Arguments:
  ROOT_DIR  root directory  [required]

Options:
  --config-file TEXT              config file path (default: first '.jinja-
                                  tree.toml' file found up from current
                                  working dir), can also be see with
                                  JINJA_TREE_CONFIG_FILE env var
  --log-level TEXT                log level (DEBUG, INFO, WARNING or ERROR)
                                  [default: INFO]
  --extra-search-path PATH        Search path to jinja
  --add-cwd-to-search-path / --no-add-cwd-to-search-path
                                  add current working directory (CWD) to jinja
                                  search path
  --add-root-dir-to-search-path / --no-add-root-dir-to-search-path
                                  add root directory to jinja search path
  --jinja-extension TEXT          jinja extension to load
  --context-plugin TEXT           context plugin (full python class path)
  --file-action-plugin TEXT       file-action plugin (full python class path)
  --strict-undefined / --no-strict-undefined
                                  if set, raise an error if a variable does
                                  not exist in context
  --blank-run / --no-blank-run    if set, execute a blank run (without
                                  modifying or deleting anything)  [default:
                                  no-blank-run]
  --delete-original / --no-delete-original
                                  delete original file
  --replace / --no-replace        replace target file event if exists
  --disable-embedded-jinja-extensions / --no-disable-embedded-jinja-extensions
                                  disable embedded jinja extensions
  --help                          Show this message and exit.

```

## Bonus

Another CLI utility is provided to process a Jinja template given as stdin: 


```console
$ export FOO=bar
$ echo "Hello {{FOO}}" | jinja-stdin
Hello bar
```


Full help of this bonus CLI utility:

```
$ jinja-stdin --help 
Usage: cli_stdin.py [OPTIONS]

Options:
  --config-file TEXT              config file path (default: first '.jinja-
                                  tree.toml' file found up from current
                                  working dir), can also be see with
                                  JINJA_TREE_CONFIG_FILE env var
  --log-level TEXT                log level (DEBUG, INFO, WARNING or ERROR)
                                  [default: INFO]
  --extra-search-path PATH        Search path to jinja
  --add-cwd-to-search-path / --no-add-cwd-to-search-path
                                  add current working directory (CWD) to jinja
                                  search path
  --jinja-extension TEXT          jinja extension to load
  --context-plugin TEXT           context plugin (full python class path)
  --strict-undefined / --no-strict-undefined
                                  if set, raise an error if a variable does
                                  not exist in context
  --disable-embedded-jinja-extensions / --no-disable-embedded-jinja-extensions
                                  disable embedded jinja extensions
  --help                          Show this message and exit.

```