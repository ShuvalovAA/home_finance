FROM cr.yandex/crp0civq107m91j8p8a2/base/python:3.8

RUN mkdir /app

WORKDIR /app

COPY ./pyproject.toml /app/
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/

# Poetry can't lock packages inside container because of "Exceeded 30 redirects" error.
# https://github.com/python-poetry/poetry/issues/728
COPY ./poetry.lock /app/

RUN pip install --upgrade pip \
    && pip install poetry

ARG pypi_user
ARG pypi_pass
ARG pypi_cert=/etc/ssl/certs/sailplay.pem

RUN poetry config http-basic.sailplay-pypi $pypi_user $pypi_pass \
    && poetry config certificates.sailplay-pypi.cert $pypi_cert

RUN poetry install --no-root --only=main

RUN mkdir -p /tmp/changeset
COPY ./src /app/
