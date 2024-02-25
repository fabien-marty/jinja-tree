import os
import shutil
import sys

import stlog

from jinja_tree.app.action import (
    ActionService,
    IgnoreDirectoryAction,
    IgnoreFileAction,
    ProcessFileAction,
    RenameFileAction,
)
from jinja_tree.app.config import Config
from jinja_tree.app.jinja import JinjaService

IGNORE_FILENAME = ".jinja-tree-ignore"
logger = stlog.getLogger("jinja-tree")


def get_source_content(source_absolute_path: str) -> str:
    with open(source_absolute_path) as f:
        return f.read()


def get_target_content(target_absolute_path: str) -> str:
    with open(target_absolute_path) as f:
        return f.read()


def set_target_content(
    target_absolute_path: str,
    content: str,
    source_absolute_path: str,
    blank_run: bool = False,
):
    if (
        os.path.isfile(target_absolute_path)
        and get_target_content(target_absolute_path) == content
    ):
        logger.debug("No change to apply to the target file", path=target_absolute_path)
        return
    if blank_run:
        print(
            f"[BLANK RUN] Fake setting new content for {target_absolute_path}",
            file=sys.stderr,
        )
        print("[BLANK RUN]<new_content>", file=sys.stderr)
        print(content)
        print("[BLANK RUN]</new_content>", file=sys.stderr)
        return
    logger.info(
        "New content written to target file",
        path=target_absolute_path,
        source_path=source_absolute_path,
    )
    with open(target_absolute_path, "w") as f:
        f.write(content)


def delete_source_file(filepath: str, blank_run: bool = False):
    if blank_run:
        print(f"[BLANK RUN] Fake deleting {filepath}...", file=sys.stderr)
    else:
        logger.info("Deleting a file", path=filepath)
        os.unlink(filepath)


class JinjaTreeService:
    """
    A service class for processing tree of files using Jinja templates.

    Args:
        config: The configuration object.
        action_service: The Action service.
        jinja_service: The JinjaService object to render single strings.
        blank_run: Flag indicating if it is a blank run.
    """

    def __init__(
        self,
        config: Config,
        action_service: ActionService,
        jinja_service: JinjaService,
        blank_run: bool = False,
    ):
        self.config = config
        self.action_service = action_service
        self.jinja_service = jinja_service
        self.blank_run = blank_run

    def trace(self, msg: str, **kwargs):
        if self.config.verbose:
            logger.debug(msg, **kwargs)

    def chdir(self, dirpath: str):
        self.trace("Changing working directory", new_path=dirpath)
        os.chdir(dirpath)

    def do_process_action(self, action: ProcessFileAction):
        if self.config.change_cwd:
            self.chdir(action.dirpath)
        content = get_source_content(action.source_absolute_path)
        logger.debug(
            "Processing a file",
            path=action.source_absolute_path,
            target=action.target_absolute_path,
        )
        result = self.jinja_service.render_string(content, action.source_absolute_path)
        set_target_content(
            action.target_absolute_path,
            result,
            action.source_absolute_path,
            blank_run=self.blank_run,
        )
        if action.delete_original:
            delete_source_file(action.source_absolute_path, blank_run=self.blank_run)

    def do_rename_action(self, action: RenameFileAction):
        if self.blank_run:
            print(
                f"[BLANK RUN] Fake renaming {action.source_absolute_path} to {action.target_absolute_path}...",
                file=sys.stderr,
            )
        else:
            logger.info(
                f"Renaming {action.source_absolute_path} to {action.target_absolute_path}..."
            )
            shutil.move(action.source_absolute_path, action.target_absolute_path)

    def process(self):
        for dirpath, dirnames, filenames in os.walk(self.config.root_dir, topdown=True):
            # Check if the directory should be ignored because of IGNORE_FILENAME
            if IGNORE_FILENAME in filenames:
                self.trace(
                    f"Ignored directory because {IGNORE_FILENAME} found (inside)",
                    path=dirpath,
                )
                # modify in-place, see https://stackoverflow.com/a/19859907
                # to ignore recursively
                dirnames[:] = []
                continue

            # Directory action
            dir_action = self.action_service.get_directory_action(dirpath)
            if isinstance(dir_action, IgnoreDirectoryAction):
                # modify in-place, see https://stackoverflow.com/a/19859907
                # to ignore recursively
                dirnames[:] = []
                continue

            # File actions
            for f in filenames:
                path = os.path.join(dirpath, f)
                action = self.action_service.get_file_action(path)
                if isinstance(action, IgnoreFileAction):
                    pass
                elif isinstance(action, ProcessFileAction):
                    try:
                        self.do_process_action(action)
                    except Exception:
                        logger.error(
                            "An error occurred while processing the file",
                            path=action.source_absolute_path,
                        )
                        raise
                elif isinstance(action, RenameFileAction):
                    self.do_rename_action(action)
                else:
                    raise Exception("unknown action type: %s", action)
