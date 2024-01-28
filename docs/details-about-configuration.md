<!-- *** GENERATED FILE - DO NOT EDIT *** -->
<!-- To modify this file, edit docs/details-about-configuration.md.template and launch 'make doc' -->

# Details about configuration

You have two options to configure the `jinja-tree`:

- the first one is to provide configuration options with CLI options
- the second one is to provide a configuration file `.jinja-tree.toml` 

> [!IMPORTANT]
> CLI options have higher priority than configuration file.
>
> But there are only CLI options for "general" configuration (not for "plugin specific" configuration). **So you have more options in the configuration file**

## CLI options

<details>

<summary>CLI options reference of the `jinja-tree` CLI</summary>

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
  --extra-search-path PATH        Search path to jinja
  --add-cwd-to-search-path / --no-add-cwd-to-search-path
                                  add current working directory (CWD) to jinja
                                  search path
  --add-root-dir-to-search-path / --no-add-root-dir-to-search-path
                                  add root directory to jinja search path
  --jinja-extension TEXT          jinja extension to load
  --context-plugin TEXT           context plugin (full python class path)
  --action-plugin TEXT            action plugin (full python class path)
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

<details>

<summary>CLI options reference of the `jinja-stdin` bonus CLI</summary>

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

</details>

## Configuration file

### How the configuration file is found?

- if you set the `--config-file` CLI option, the configuration file is the one you set
- if the environment variable `JINJA_TREE_CONFIG_FILE` is set, the configuration file is the one set in this environment variable value
- otherwise, the configuration file is the first `.jinja-tree.toml` file found up from current working directory (we recursively search up from current working directory)

> [!TIP]
> The most common way to use the configuration file is to put it in the root directory of your project/repository. Its name must be `.jinja-tree.toml`.

### Reference (with all keys and default values)

<details>

<summary>Configuration file reference</summary>

[Full file example](jinja-tree.toml):

```toml
#############################
### General configuration ###
#############################
# (Note: all values here are the default values)

[general]

# Search paths to jinja"
extra_search_paths = []

# Add root dir to search path (if true)
add_root_dir_to_search_path = true

# Add current working dir (CWD at script start) to search path (if true)
add_cwd_to_search_path = true

# Add processed file dir to search path (if true)
add_processed_file_dir_to_search_path = false

# Change working directory when tree walking (if true)
change_cwd = true

# Crash when templates use undefined variables (if true)
strict_undefined = true

# Disable embedded jinja extensions (if true)
# List of embedded jinja extensions (for information only):
# - jinja_tree.app.embedded_extensions.from_json.FromJsonExtension
# - jinja_tree.app.embedded_extensions.shell.ShellExtension
# - jinja_tree.app.embedded_extensions.fnmatch.FnMatchExtension
# - jinja_tree.app.embedded_extensions.double_quotes.DoubleQuotesExtension
disable_embedded_jinja_extensions = false

# Jinja extensions to add (full paths)
# Notes: 
# - jinja-tree provides embedded extensions which will be added automatically to this list
# - you can disable embedded extensions with 'disable_embedded_jinja_extensions = true'
jinja_extensions = []


####################################  
### Context plugin configuration ###
####################################  
[context]

# Plugin full classpath [common key for all context plugins]
plugin = "jinja_tree.infra.adapters.context.EnvContextAdapter"

# Generated comment template: line1 [common key for all context plugins]
# Available placeholders: {utcnow}, {absolute_path}, {dirname}, {basename}, {relative_filepath}
generated_comment_line1 = "*** GENERATED FILE - DO NOT EDIT ***"

# Generated comment template: line2 [common key for all context plugins]
# Available placeholders: {utcnow}, {absolute_path}, {dirname}, {basename}, {relative_filepath}
generated_comment_line2 = "This file was generated by jinja-tree (https://github.com/fabien-marty/jinja-tree) from the template file: {{relative_filepath}}"

# Fnmatch patterns (for environment variable names) to ignore [specific to EnvContextAdapter plugin]
# Example: ["FOO*", "*BAR"]  for ignoring all env var starting with FOO or ending with BAR
env_ignores = []

# dotenv file path (absolute or relative), if set to an empty string (""), dotenv support is disabled [specific to EnvContextAdapter plugin]
dotenv_path = ".env"

# Fnmatch patterns (for dotenv variable names) to ignore [specific to EnvContextAdapter plugin]
# Example: ["FOO*", "*BAR"]  for ignoring all dotenv var starting with FOO or ending with BAR
dotenv_ignores = []

# Fnmatch patterns (for plugin_configuration variable names) to ignore [specific to EnvContextAdapter plugin]
# Example: ["foo*", "*bar"]  for ignoring all plugin configuration var starting with foo or ending with bar
plugin_configuration_ignores = ["plugin", "generated_comment_line1", "generated_comment_line2", "env_ignores", "dotenv_path", "dotenv_ignores", "plugin_configuration_ignores"]

# With the EnvContextAdapter plugin, you can add key/values below, they will be available in Jinja2 context

# [...]


########################################  
### File-action plugin configuration ###
########################################
[action]

# Plugin full classpath [common key for all action plugins]
plugin = "jinja_tree.infra.adapters.action.ExtensionsFileActionAdapter"

# File extensions to process [specific to ExtensionsFileActionAdapter plugin]
# Example: [".j2", ".jinja2", ".template"] for processing all files ending with .j2, .jinja2 or .template
extensions = [".template"]

# Filename patterns to ignore (fnmatch patterns to match against basename only)
# [specific to ExtensionsFileActionAdapter plugin]
filename_ignores = [ ".*" ]

# Dirname patterns to ignore recursively (fnmatch patterns to match against dirname only)
# [specific to ExtensionsFileActionAdapter plugin]
dirname_ignores =  [ "venv", "site-packages", "__pypackages__", "node_modules", "__pycache__", ".*" ]

# Replace target files if they already exist (if true)
# [specific to ExtensionsFileActionAdapter plugin]
replace = true

# Delete original (template) file after processing (if true)
# [specific to ExtensionsFileActionAdapter plugin]
delete_original = false
```

</details>

Go back to [main README](../README.md) file.