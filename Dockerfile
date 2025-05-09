FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c

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
