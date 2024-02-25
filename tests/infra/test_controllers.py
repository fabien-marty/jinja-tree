import os

import pytest
from typer.testing import CliRunner

from jinja_tree.infra.controllers.cli_stdin import app as app_stdin
from jinja_tree.infra.controllers.cli_tree import app as app_tree

runner = CliRunner()


def test_tree():
    result = runner.invoke(app_tree, ["--blank-run", "."])
    assert result.exit_code == 0


@pytest.fixture()
def fake_env():
    os.environ["JINJA_TREE_FOO"] = "BAR"
    yield
    os.environ.pop("JINJA_TREE_FOO")


def test_stdin(fake_env):
    result = runner.invoke(app_stdin, [], input="FOO{{JINJA_TREE_FOO}}")
    assert result.exit_code == 0
    assert result.stdout == "FOOBAR\n"
