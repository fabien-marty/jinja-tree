import sys

import typer
import typer.core

from jinja_tree.app.context import ContextService
from jinja_tree.app.jinja import JinjaService
from jinja_tree.infra.controllers.cli_common import (
    AddCwdDirToSearchPathType,
    ConfigFileType,
    ContextPluginType,
    DisableEmbeddedExtensions,
    ExtensionType,
    ExtraSearchPathsType,
    LogLevelType,
    StrictUndefinedType,
    config_dump,
    get_config,
    setup_logger,
)
from jinja_tree.infra.utils import (
    make_context_adapter_from_config,
)

# disable rich usage in typer
typer.core.rich = None  # type: ignore
app = typer.Typer(add_completion=False)


@app.command()
def pipe(
    config_file: ConfigFileType = None,
    log_level: LogLevelType = "INFO",
    extra_search_path: ExtraSearchPathsType = None,
    add_cwd_to_search_path: AddCwdDirToSearchPathType = None,
    jinja_extension: ExtensionType = None,
    context_plugin: ContextPluginType = None,
    strict_undefined: StrictUndefinedType = None,
    disable_embedded_jinja_extensions: DisableEmbeddedExtensions = None,
):
    """
    Process the standard input with Jinja templating system and return the result on the standard output.

    """
    setup_logger(log_level)
    config = get_config(
        config_file_path=config_file,
        extra_search_path=extra_search_path,
        context_plugin=context_plugin,
        add_cwd_to_search_path=add_cwd_to_search_path,
        jinja_extension=jinja_extension,
        strict_undefined=strict_undefined,
        disable_embedded_jinja_extensions=disable_embedded_jinja_extensions,
    )
    if log_level == "DEBUG":
        config_dump(config)
    context_adapter = make_context_adapter_from_config(config)
    context_service = ContextService(config=config, adapter=context_adapter)
    jinja_service = JinjaService(config=config, context_service=context_service)
    print(jinja_service.render_string(sys.stdin.read()))


if __name__ == "__main__":
    app()
