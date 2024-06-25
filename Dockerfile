FROM python:3.12.4-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y curl

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock /app/
COPY ./alembic.ini /app/

ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install; else poetry install --only main ; fi"
