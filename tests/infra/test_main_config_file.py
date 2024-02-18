import os

from jinja_tree.infra.utils import read_config_file_or_die

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_CONFIG_FILE_PATH = os.path.join(SCRIPT_DIR, "..", "..", "docs", "jinja-tree.toml")


def test_main_config_file():
    read_config_file_or_die(MAIN_CONFIG_FILE_PATH)
