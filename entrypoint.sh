#!/bin/sh

cd /app || exit 1
exec ./.tmp/bin/uv run --locked --no-sync jinja-tree "$@"


