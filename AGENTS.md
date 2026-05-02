# AGENTS.md

This document provides essential context and guidelines for AI agents working on the jinja-tree repository.

## Overview

`jinja-tree` is a Python CLI that renders Jinja templates across a directory tree.

The default workflow is:

- walk a root directory recursively
- identify template files through action plugins (by default, files ending with `.template`)
- build a rendering context from multiple context plugins
- render each matching file through Jinja2
- write the rendered result to the target path, optionally deleting or renaming source files depending on plugin behavior

The repository also ships a second CLI, `jinja-stdin`, which renders a single template received on standard input using the same configuration and context system.

The codebase is organized around a small application layer (`jinja_tree/app`) containing core services and plugin interfaces, and an infrastructure layer (`jinja_tree/infra`) containing default adapters and CLI entrypoints.

### Key libraries

- `jinja2`: template engine used for rendering files and stdin input, including support for custom extensions, includes, and inheritance
- `typer`: CLI framework used by `jinja-tree` and `jinja-stdin`
- `stlog`: structured logging used across the application
- `dataclasses-json`: parsing and validation for config and plugin-specific dataclasses
- `tomli`: TOML parsing for configuration and TOML-backed context input
- `python-dotenv`: loading context values from dotenv files
- `pytest`: test runner
- `ruff`: formatting and linting
- `ty`: static type checking

## Directives

### Execute linting systematically (style, type checking...)

- After each change, execute `make lint || echo "FAILED"` to execute all these linting tools. This execution can autofix some issues.
- If the last line of the output is "FAILED", fix the issues and re-run the linting until it succeeds.

### Execute tests

- After each python code change, execute `make test || echo "FAILED"` to execute all unit tests.
- If the last line of the output is "FAILED", fix the issues and re-run the tests until it succeeds.
- You can execute a specific test file with `uv run pytest tests/common/source_config/test_service.py` for example.

### Makefile targets

- `make sync` — Sync dependencies with uv
- `make lint` — Run all linters (ruff check + format, ty check, import-linter)
- `make test` — Run all tests
- `make clean` — Clean build artifacts

## Architecture

High-level flow:

- CLI controllers in `jinja_tree/infra/controllers/` parse options, load configuration, instantiate services and adapters, then trigger processing
- `Config` in `jinja_tree/app/config.py` holds global behavior and default plugin lists
- `ContextService` in `jinja_tree/app/context.py` merges context from configured `ContextPort` adapters and injects built-in metadata such as file path and generated-file comments
- `JinjaService` in `jinja_tree/app/jinja.py` builds the Jinja environment, configures loaders/search paths, and renders template content
- `ActionService` in `jinja_tree/app/action.py` asks configured `ActionPort` adapters what to do for each directory and file
- `JinjaTreeService` in `jinja_tree/app/jinja_tree.py` walks the filesystem and executes the selected actions

Default adapters:

- `jinja_tree/infra/adapters/context.py` provides context from TOML files, config values, environment variables, and dotenv files
- `jinja_tree/infra/adapters/action.py` provides the default extension-based file selection logic

Plugin model:

- context plugins implement `ContextPort` and return dictionaries merged into the final Jinja context
- action plugins implement `ActionPort` and decide whether a path is ignored, rendered, or renamed
- plugin classes are referenced by full Python import path in config

Important built-in behavior:

- embedded Jinja extensions are enabled by default from `jinja_tree/app/embedded_extensions/`
- the default action plugin processes files ending in `.template`
- directories such as `venv`, `node_modules`, `__pycache__`, and hidden directories are ignored by default
- a `.jinja-tree-ignore` file causes the matching directory subtree to be skipped entirely
