FROM alpine:3.21

ENV TASK=go-task
ENV UV_NO_CACHE=1

RUN apk update && apk upgrade && apk add bash go-task make && rm -rf /var/cache/apk/*
RUN mkdir -p /app
COPY .task /app/.task
COPY Taskfile.yml README.md pyproject.toml uv.lock /app/
RUN cd /app && export UV_SYNC_OPTS="--frozen --no-dev --no-install-project" && $TASK install
COPY jinja_tree /app/jinja_tree/
COPY entrypoint.sh entrypoint-stdin.sh /app/
RUN cd /app && export UV_SYNC_OPTS="--frozen --no-dev" && $TASK install

ENTRYPOINT ["/app/entrypoint.sh"]
