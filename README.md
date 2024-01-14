<-- *** GENERATED FILE - DO NOT EDIT *** -->
<-- To modify this file, edit README.md.template and launch 'make doc' -->

# jinja-tree

CLI to process jinja (jinja2) templates in a directory tree

```
Usage: jinja-tree [OPTIONS] ROOT_DIR

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


```
Usage: jinja-stdin [OPTIONS]

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