import os
from typing import Iterator

import stlog

from jinja_tree.app.config import Config
from jinja_tree.app.file_action import (
    FileActionService,
    ProcessFileAction,
)
from jinja_tree.app.jinja import JinjaService
from jinja_tree.infra.utils import is_fnmatch_ignored

IGNORE_FILENAME = ".jinja-tree-ignore"

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
    if get_target_content(target_absolute_path) == content:
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
        file_action_service: FileActionService,
        jinja_service: JinjaService,
        blank_run: bool = False,
    ):
        self.config = config
        self.file_action_service = file_action_service
        self.jinja_service = jinja_service
        self.blank_run = blank_run

    def file_absolute_paths(self) -> Iterator[str]:
        for dirpath, dirnames, filenames in os.walk(self.config.root_dir, topdown=True):
            exclude_file = os.path.join(dirpath, IGNORE_FILENAME)
            if is_fnmatch_ignored(
                os.path.basename(dirpath), self.config.dirname_ignores
            ):
                logger.debug(
                    "Ignored directory because of dirname_ignores configuration value",
                    path=dirpath,
                )
                # modify in-place, see https://stackoverflow.com/a/19859907
                # to ignore recursively
                dirnames[:] = []
                continue
            if os.path.isfile(exclude_file):
                logger.debug(
                    f"Ignored directory tree because of presence of {IGNORE_FILENAME}",
                    path=dirpath,
                )
                # modify in-place, see https://stackoverflow.com/a/19859907
                # to ignore recursively
                dirnames[:] = []
                continue
            for f in filenames:
                path = os.path.join(dirpath, f)
                if is_fnmatch_ignored(f, self.config.filename_ignores):
                    logger.debug(
                        "Ignored file because of ignores configuration value",
                        path=path,
                    )
                    continue
                yield path

    def actions(self) -> Iterator[ProcessFileAction]:
        for path in self.file_absolute_paths():
            action = self.file_action_service.get_action(path)
            if not isinstance(action, ProcessFileAction):
                logger.debug("Ignored file", path=path)
                continue
            yield action

    def process_action(self, action: ProcessFileAction):
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

    def process(self):
        for action in self.actions():
            self.process_action(action)
