#!/bin/sh

export UV="/app/.tmp/taskfile-python-uv/uv/uv"

if ! test -d /code; then
  if test -d /workdir; then
    # DEPRECATED: only for smooth transition
    echo "WARNING: usage of /workdir is DEPRECATED => replace /workdir by /code"
    cd /workdir || exit 1
  fi
else
  cd /code
fi
exec "${UV}" run /app/.venv/bin/jinja-stdin "$@"
