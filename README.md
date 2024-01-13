<-- *** GENERATED FILE - DO NOT EDIT *** -->
<-- To modify this file, edit README.md.template and launch 'make doc' -->

# jinja-tree

CLI to process jinja (jinja2) templates in a directory tree

```
                                                                                                                                                                                                           
 Usage: jinja-tree [OPTIONS] ROOT_DIR                                                                                                                                                                      
                                                                                                                                                                                                           
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    root_dir      PATH  root directory [default: None] [required]                                                                                                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --config-file                                                                    TEXT  config file path (default: first '.jinja-tree.toml' file found up from current working dir), can also be see     │
│                                                                                        with JINJA_TREE_CONFIG_FILE env var                                                                              │
│                                                                                        [default: None]                                                                                                  │
│ --log-level                                                                      TEXT  log level (DEBUG, INFO, WARNING or ERROR) [default: INFO]                                                        │
│ --extra-search-path                                                              PATH  Search path to jinja [default: None]                                                                             │
│ --add-cwd-to-search-path               --no-add-cwd-to-search-path                     add current working directory (CWD) to jinja search path [default: no-add-cwd-to-search-path]                    │
│ --add-root-dir-to-search-path          --no-add-root-dir-to-search-path                add root directory to jinja search path [default: no-add-root-dir-to-search-path]                                │
│ --jinja-extension                                                                TEXT  jinja extension to load [default: None]                                                                          │
│ --context-plugin                                                                 TEXT  context plugin (full python class path) [default: None]                                                          │
│ --file-action-plugin                                                             TEXT  file-action plugin (full python class path) [default: None]                                                      │
│ --strict-undefined                     --no-strict-undefined                           if set, raise an error if a variable does not exist in context [default: no-strict-undefined]                    │
│ --blank-run                            --no-blank-run                                  if set, execute a blank run (without modifying or deleting anything) [default: no-blank-run]                     │
│ --delete-original                      --no-delete-original                            delete original file [default: no-delete-original]                                                               │
│ --replace                              --no-replace                                    replace target file event if exists [default: no-replace]                                                        │
│ --disable-embedded-jinja-extensions    --no-disable-embedded-jinja-extensions          disable embedded jinja extensions [default: no-disable-embedded-jinja-extensions]                                │
│ --help                                                                                 Show this message and exit.                                                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


```


```
                                                                                                                                                                                                           
 Usage: jinja-stdin [OPTIONS]                                                                                                                                                                              
                                                                                                                                                                                                           
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --config-file                                                                    TEXT  config file path (default: first '.jinja-tree.toml' file found up from current working dir), can also be see     │
│                                                                                        with JINJA_TREE_CONFIG_FILE env var                                                                              │
│                                                                                        [default: None]                                                                                                  │
│ --log-level                                                                      TEXT  log level (DEBUG, INFO, WARNING or ERROR) [default: INFO]                                                        │
│ --extra-search-path                                                              PATH  Search path to jinja [default: None]                                                                             │
│ --add-cwd-to-search-path               --no-add-cwd-to-search-path                     add current working directory (CWD) to jinja search path [default: no-add-cwd-to-search-path]                    │
│ --jinja-extension                                                                TEXT  jinja extension to load [default: None]                                                                          │
│ --context-plugin                                                                 TEXT  context plugin (full python class path) [default: None]                                                          │
│ --strict-undefined                     --no-strict-undefined                           if set, raise an error if a variable does not exist in context [default: no-strict-undefined]                    │
│ --disable-embedded-jinja-extensions    --no-disable-embedded-jinja-extensions          disable embedded jinja extensions [default: no-disable-embedded-jinja-extensions]                                │
│ --help                                                                                 Show this message and exit.                                                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


```