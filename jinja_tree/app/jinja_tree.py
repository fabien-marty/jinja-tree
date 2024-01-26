import os
import shutil

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

logger = stlog.getLogger("jinja-tree")


def get_source_content(source_absolute_path: str) -> str:
    with open(source_absolute_path) as f:
        return f.read()


def get_target_content(target_absolute_path: str) -> str:
    with open(target_absolute_path) as f:
        return f.read()


def set_target_content(
    target_absolute_path: str, content: str, blank_run: bool = False
):
    if (
        os.path.isfile(target_absolute_path)
        and get_target_content(target_absolute_path) == content
    ):
        logger.info("No change to apply to the target file", path=target_absolute_path)
        return
    if blank_run:
        print(f"[BLANK RUN] Fake setting new content for {target_absolute_path}")
        print("[BLANK RUN]<new_content>")
        print(content)
        print("[BLANK RUN]</new_content>")
        return
    logger.info("New content written to target file", path=target_absolute_path)
    with open(target_absolute_path, "w") as f:
        f.write(content)


def delete_source_file(filepath: str, blank_run: bool = False):
    if blank_run:
        print(f"[BLANK RUN] Fake deleting {filepath}...")
    else:
        logger.info("Deleting a file", path=filepath)
        os.unlink(filepath)


def chdir(dirpath: str):
    logger.debug("Changing working directory", new_path=dirpath)
    os.chdir(dirpath)


class JinjaTreeService:
    """
    A service class for processing tree of files using Jinja templates.

    Args:
        config: The configuration object.
        file_action_service: The FileAction service.
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

    def do_process_action(self, action: ProcessFileAction):
        if self.config.change_cwd:
            chdir(action.dirpath)
        content = get_source_content(action.source_absolute_path)
        logger.info(
            "Processing a file",
            path=action.source_absolute_path,
            target=action.target_absolute_path,
        )
        result = self.jinja_service.render_string(content, action.source_absolute_path)
        set_target_content(
            action.target_absolute_path, result, blank_run=self.blank_run
        )
        if action.delete_original:
            delete_source_file(action.source_absolute_path, blank_run=self.blank_run)

    def do_rename_action(self, action: RenameFileAction):
        if self.blank_run:
            print(
                f"[BLANK RUN] Fake renaming {action.source_absolute_path} to {action.target_absolute_path}..."
            )
        else:
            logger.info(
                f"Renaming {action.source_absolute_path} to {action.target_absolute_path}..."
            )
            shutil.move(action.source_absolute_path, action.target_absolute_path)

    def process(self):
        for dirpath, dirnames, filenames in os.walk(self.config.root_dir, topdown=True):
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
                    self.do_process_action(action)
                elif isinstance(action, RenameFileAction):
                    self.do_rename_action(action)
                else:
                    raise Exception("unknown action type: %s", action)
