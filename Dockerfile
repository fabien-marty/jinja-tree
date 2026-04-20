FROM alpine:3.23@sha256:5b10f432ef3da1b8d4c7eb6c487f2f5a8f096bc91145e68878dd4a5019afde11

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:c4f5de312ee66d46810635ffc5df34a1973ba753e7241ce3a08ef979ddd7bea5 /uv /uvx /bin/

ENV UV_NO_CACHE=1
ENV UV_PYTHON_INSTALL_DIR=/python

RUN apk update && apk upgrade && apk add bash make && rm -rf /var/cache/apk/*
RUN mkdir -p /app
COPY Makefile README.md pyproject.toml uv.lock /app/
RUN cd /app && export UV_SYNC_OPTS="--frozen --no-dev --no-install-project" && make install
COPY jinja_tree /app/jinja_tree/
COPY entrypoint.sh entrypoint-stdin.sh /app/
RUN cd /app && export UV_SYNC_OPTS="--frozen --no-dev" && make install

ENTRYPOINT ["/app/entrypoint.sh"]
