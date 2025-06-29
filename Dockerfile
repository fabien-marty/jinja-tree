FROM alpine:3.22@sha256:8a1f59ffb675680d47db6337b49d22281a139e9d709335b492be023728e11715

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
