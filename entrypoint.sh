#!/bin/sh

cd /code || exit 1
exec /app/.tmp/bin/uv run /app/.venv/bin/jinja-tree "$@"


