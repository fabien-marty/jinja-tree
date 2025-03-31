FROM python:3.12-alpine

ENV TASK=go-task
ENV UV_NO_CACHE=1

RUN apk update && apk upgrade && apk add go-task && rm -rf /var/cache/apk/*
RUN mkdir -p /app
COPY .task /app/.task
COPY Taskfile.yml README.md pyproject.toml uv.lock /app/
RUN cd /app && export UV_SYNC_OPTS="--frozen --no-dev --no-install-project" && $TASK install
COPY jinja_tree /app/jinja_tree/
COPY entrypoint.sh /app/entrypoint.sh
RUN cd /app && export UV_SYNC_OPTS="--frozen --no-dev --verbose" && $TASK install

ENTRYPOINT ["/app/entrypoint.sh"]
