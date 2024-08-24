FROM python:3.12-slim-bookworm

RUN apt update && apt -y install make
RUN pip install jinja-tree rich

RUN mkdir /workdir
WORKDIR /workdir

ENTRYPOINT ["jinja-tree"]
