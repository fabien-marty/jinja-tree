<!-- *** GENERATED FILE - DO NOT EDIT *** -->
<!-- To modify this file, edit docs/details-about-plugins.md.template and launch 'make doc' -->

# Details about plugins

In `jinja-tree` there are two extension points:

- one for providing context variables to Jinja templates (let's call it `context`)
- one for providing actions to do on files or directories (let's call in `action`)

`jinja-tree` default behavior is driven by two plugins:

- `jinja_tree.infra.adapters.context.EnvContextAdapter` (for the `context` extension point)
- `jinja_tree.infra.adapters.action.ExtensionsFileActionAdapter`(for the `action` extension point)

Of course, you can provide your own plugins to override the default behavior by passing your class full path to the `--context-plugin` or `--action-plugin` CLI options (or corresponding configuration file keys).

## Context plugins

The role of the context plugin is to provide some context variables for Jinja template processing.

It's a class that must implement the `jinja_tree.app.context.ContextPort` interface.

<details>

<summary>Details of the ContextPort interface</summary>

```python
class ContextPort(ABC):
    """This is the abstract interface for ContextPort adapters."""

    @abstractmethod
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        """
        Construct a new ContextPort object given a configuration object
        and a plugin configuration dict.

        Args:
            config (Config): The configuration object.
            plugin_config (Dict[str, Any]): The plugin configuration dict.

        """
        pass

    @abstractmethod
    def get_context(self) -> Dict[str, Any]:
        """
        Retrieve the Jinja context to apply.

        Note: it can depends on the current working directory (CWD).

        Returns:
            The context dictionary.

        """
        pass

    @classmethod
    @abstractmethod
    def get_config_name(cls) -> str:
        """
        Return the name of the configuration object.

        For example, if we return "foo", it means that the configuration in the TOML file
        is located under:

        [context.foo]
        # ... some configuration ...

        Returns:
            The name of the configuration object.

        """
        pass

```

</details>

A higher-level service object will add to the context returned by the plugin some extra keys:

- `JINJA_TREE = "1"`
- `JINJA_DT = "2024-01-25T12:34:56Z"`
- `JINJA_TREE_FILEPATH = "/foo/bar/baz.py"`
- `JINJA_TREE_DIRNAME = "/foo/bar"`
- `JINJA_TREE_BASENAME = "baz.py"`
- `JINJA_TREE_ROOT_DIR = "/foo"`
- `JINJA_TREE_RELATIVE_FILEPATH = "bar/baz.py"`
- `JINJA_TREE_STYLE1_GENERATED_COMMENT = "<!-- ... -->"`
- `JINJA_TREE_STYLE2_GENERATED_COMMENT = "# ..."`
- `JINJA_TREE_STYLE3_GENERATED_COMMENT = "// ..."`

> ![NOTE]
> `JINJA_TREE_STYLE{1,2,3}_GENERATED_COMMENT` are comments you can add
> to your generated files to say "hey this is the generated file => do not modify it!".
>
> You can use the style of comments you need (depending on the file type you generate). And
> you can also configure the message itself.

### The default context plugin

The [default context plugin](../jinja_tree/infra/adapters/context.py) provides a context by merging 3 layers of contexts (in this order):

- the "configuration context" you can provide by adding some extra key/values in the `.jinja-tree.toml` configuration file
- the "environment variables context" you can provide by setting some environment variables
- the "dotenv" context you can provide by adding some extra key/values in a dotenv file

Of course, you can configure plenty of things to tune this default behavior.

### Other context plugins

To manage this repository, we use a [custom context plugin](../tools/jinja_tree_plugins_context.py) that is very specific to this repository
but this is maybe a good example to show you how to write your own context plugin.

## Action plugins

The role of the `action` plugin is to provide actions to do on files or directories. 

> [!NOTE]
> The `action` plugin returns actions to do on the file or directory. It does not do the action itself.

It's a class that must implement the `jinja_tree.app.context.ActionPort` interface.

<details>

<summary>Details of the ActionPort interface</summary>

### Interface to implement

```python
class ActionPort(ABC):
    """This is the abstract interface for FileActionPort adapters."""

    @abstractmethod
    def __init__(self, config: Config, plugin_config: Dict[str, Any]):
        """
        Construct a new FileActionPort object given a configuration object
        and a plugin configuration dict.

        Args:
            config (Config): The configuration object.
            plugin_config (Dict[str, Any]): The plugin configuration dict.

        """
        pass

    @classmethod
    @abstractmethod
    def get_config_name(cls) -> str:
        """
        Return the name of the configuration object.

        For example, if we return "foo", it means that the configuration in the TOML file
        is located under:

        [action.foo]
        # ... some configuration ...

        Returns:
            The name of the configuration object.

        """
        pass

    @abstractmethod
    def get_file_action(self, absolute_path: str) -> FileAction:
        """Return the action to execute on the file at the given absolute path.

        Note:
        - absolute_path is checked to be a file before calling this method.

        Attributes:
            absolute_path: absolute path for the file to process.
        """
        pass

    @abstractmethod
    def get_directory_action(self, absolute_path: str) -> DirectoryAction:
        """Return the action to execute on the directory at the given absolute path.

        Note:
        - absolute_path is checked to be a directory before calling this method.

        Attributes:
            absolute_path: absolute path for the directory to process.
        """
        pass

```

</details>

<details>

<summary>Concrete FileAction classes the plugin can return</summary>

```python
@dataclass
class IgnoreFileAction(FileAction):
    """This is a concrete implementation of FileAction to represent a "do nothing with this file" action."""

    pass


@dataclass
class ProcessFileAction(FileAction):
    """This is a concrete implementation of FileAction to represent a "process this file with jinja" action.

    Attributes:
        target_absolute_path: absolute path for the target file (the rendered file).
        delete_original: if True, the original file will be deleted after the rendering.
    """

    target_absolute_path: str
    delete_original: bool = False


@dataclass
class RenameFileAction(FileAction):
    """This is a concrete implementation of fileAction to represent a "rename this file" action."""

    target_absolute_path: str

```

</details>

<details>

<summary>Create DirectoryAction classes the plugin can return</summary>

```python
@dataclass
class IgnoreDirectoryAction(DirectoryAction):
    """This is a concrete implementation of DirectoryAction to represent a "do nothing with this directory" action.

    All files in this directory or subdirectories will be ignored (recursively).
    """

    pass


@dataclass
class BrowseDirectoryAction(DirectoryAction):
    """This is a concrete implementation of DirectoryAction to represent a "browse this directory" action.

    The directory itself won't be changed but all files and subdirectories will be scanned for actions.
    """

    pass

```

</details>

## The default action plugin

The [default action plugin](../jinja_tree/infra/adapters/action.py) has the following behavior.

### For directories

- it checks if the directory name matches the fnmatch pattern provided `dirname_ignores` configuration key
    - if it matches, the directory (and recursively all this content) is ignored
- it checks if there is a `.jinja-tree-ignore` file in the directory
    - if there is one, the directory (and recursively all this content) is ignored
- else the directory is flagged to be recursively browsed

### For files

- if checks if the filename matches the fnmatch pattern provided by the `filename_ignores` configuration key
    - if it matches, the file is ignored
- if checks if the filename extension is one of the extensions provided by the `extensions` configuration key
    - if it doesn't match, the file is ignored
- else the file is flagged to be processed with "Jinja2" with a target filename that is the same as the original filename but with the extension removed

Go back to [main README](../README.md) file.