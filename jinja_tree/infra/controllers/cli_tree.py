import stlog
import typer
import typer.core

from jinja_tree.app.action import ActionService
from jinja_tree.app.context import ContextService
from jinja_tree.app.jinja import JinjaService
from jinja_tree.app.jinja_tree import JinjaTreeService
from jinja_tree.infra.controllers.cli_common import (
    AddCwdDirToSearchPathType,
    AddRootDirToSearchPathType,
    BlankRunType,
    ConfigFileType,
    ContextPluginType,
    DisableEmbeddedExtensions,
    ExtensionType,
    ExtraSearchPathsType,
    FileActionPluginType,
    LogLevelType,
    RootDirType,
    StrictUndefinedType,
    config_dump,
    get_config,
    setup_logger,
)
from jinja_tree.infra.utils import (
    make_context_adapter_from_config,
    make_file_action_adapter_from_config,
)

# disable rich usage in typer
typer.core.rich = None  # type: ignore
app = typer.Typer(add_completion=False)


@app.command()
def tree(
    root_dir: RootDirType,
    config_file: ConfigFileType = None,
    log_level: LogLevelType = "INFO",
    extra_search_path: ExtraSearchPathsType = None,
    add_cwd_to_search_path: AddCwdDirToSearchPathType = None,
    add_root_dir_to_search_path: AddRootDirToSearchPathType = None,
    jinja_extension: ExtensionType = None,
    context_plugin: ContextPluginType = None,
    action_plugin: FileActionPluginType = None,
    strict_undefined: StrictUndefinedType = None,
    blank_run: BlankRunType = False,
    disable_embedded_jinja_extensions: DisableEmbeddedExtensions = None,
):
    """
    Process a directory tree with the Jinja / Jinja2 templating system.

    """
    if log_level is not None:
        stlog.setup(level=log_level)
    config = get_config(
        config_file_path=config_file,
        extra_search_path=extra_search_path,
        add_cwd_to_search_path=add_cwd_to_search_path,
        add_root_dir_to_search_path=add_root_dir_to_search_path,
        jinja_extension=jinja_extension,
        strict_undefined=strict_undefined,
        context_plugin=context_plugin,
        action_plugin=action_plugin,
        disable_embedded_jinja_extensions=disable_embedded_jinja_extensions,
        root_dir=root_dir,
    )
    if log_level == "DEBUG":
        config_dump(config)
    setup_logger(log_level)
    context_adapter = make_context_adapter_from_config(config)
    file_action_adapter = make_file_action_adapter_from_config(config)
    context_service = ContextService(config=config, adapter=context_adapter)
    file_action_service = ActionService(config=config, adapter=file_action_adapter)
    jinja_service = JinjaService(config=config, context_service=context_service)
    jinja_tree_service = JinjaTreeService(
        config=config,
        action_service=file_action_service,
        jinja_service=jinja_service,
        blank_run=blank_run,
    )
    jinja_tree_service.process()


if __name__ == "__main__":
    app()
