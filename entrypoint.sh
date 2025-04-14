#!/bin/sh

export UV="/app/.tmp/taskfile-python-uv/uv/uv"

if ! test -d /code; then
  # DEPRECATED: only for smooth transition
  echo "WARNING: usage of /workdir is DEPRECATED => replace /workdir by /code"
  cd /workdir || exit 1
else
  cd /code
fi
exec "${UV}" run /app/.venv/bin/jinja-tree "$@"


