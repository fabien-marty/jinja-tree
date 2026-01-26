FROM alpine:3.23@sha256:865b95f46d98cf867a156fe4a135ad3fe50d2056aa3f25ed31662dff6da4eb62

ENV TASK=go-task
ENV UV_NO_CACHE=1
ENV UV_PYTHON_INSTALL_DIR=/app/.tmp/taskfile-python-uv

RUN apk update && apk upgrade && apk add bash go-task make && rm -rf /var/cache/apk/*
RUN mkdir -p /app
COPY .task /app/.task
COPY Taskfile.yml README.md pyproject.toml uv.lock /app/
RUN cd /app && export UV_SYNC_OPTS="--frozen --no-dev --no-install-project" && $TASK install
COPY jinja_tree /app/jinja_tree/
COPY entrypoint.sh entrypoint-stdin.sh /app/
RUN cd /app && export UV_SYNC_OPTS="--frozen --no-dev" && $TASK install

ENTRYPOINT ["/app/entrypoint.sh"]
