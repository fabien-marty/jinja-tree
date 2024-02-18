import typer
import typer.core

from jinja_tree.app import dump
from jinja_tree.app.action import ActionService
from jinja_tree.app.context import ContextService
from jinja_tree.app.jinja import JinjaService
from jinja_tree.app.jinja_tree import JinjaTreeService
from jinja_tree.infra.controllers.cli_common import (
    ActionPluginType,
    AddCwdDirToSearchPathType,
    AddRootDirToSearchPathType,
    BlankRunType,
    ConfigFileType,
    ContextPluginsType,
    DisableEmbeddedExtensionsType,
    ExtensionType,
    ExtraSearchPathsType,
    LogLevelType,
    RootDirType,
    StrictUndefinedType,
    VerboseType,
    get_config,
)
from jinja_tree.infra.utils import (
    make_action_adapters_from_config,
    make_context_adapters_from_config,
    setup_logger,
)

# disable rich usage in typer
typer.core.rich = None  # type: ignore
app = typer.Typer(add_completion=False)


@app.command()
def tree(
    root_dir: RootDirType,
    config_file: ConfigFileType = None,
    log_level: LogLevelType = "INFO",
    verbose: VerboseType = False,
    extra_search_path: ExtraSearchPathsType = None,
    add_cwd_to_search_path: AddCwdDirToSearchPathType = None,
    add_root_dir_to_search_path: AddRootDirToSearchPathType = None,
    jinja_extension: ExtensionType = None,
    context_plugin: ContextPluginsType = None,
    action_plugin: ActionPluginType = None,
    strict_undefined: StrictUndefinedType = None,
    blank_run: BlankRunType = False,
    disable_embedded_jinja_extensions: DisableEmbeddedExtensionsType = None,
):
    """
    Process a directory tree with the Jinja / Jinja2 templating system.

    """
    config = get_config(
        config_file_path=config_file,
        extra_search_path=extra_search_path,
        add_cwd_to_search_path=add_cwd_to_search_path,
        add_root_dir_to_search_path=add_root_dir_to_search_path,
        jinja_extension=jinja_extension,
        strict_undefined=strict_undefined,
        context_plugins=context_plugin,
        action_plugins=action_plugin,
        disable_embedded_jinja_extensions=disable_embedded_jinja_extensions,
        root_dir=root_dir,
        log_level=log_level,
        verbose=verbose,
    )
    if config.verbose:
        dump("config", config)
    setup_logger(config.log_level)
    context_adapters = make_context_adapters_from_config(config)
    action_adapters = make_action_adapters_from_config(config)
    context_service = ContextService(config=config, adapters=context_adapters)
    action_service = ActionService(config=config, adapters=action_adapters)
    jinja_service = JinjaService(config=config, context_service=context_service)
    jinja_tree_service = JinjaTreeService(
        config=config,
        action_service=action_service,
        jinja_service=jinja_service,
        blank_run=blank_run,
    )
    jinja_tree_service.process()


if __name__ == "__main__":
    app()
