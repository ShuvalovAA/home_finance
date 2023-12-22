FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY ./pyproject.toml /app/
COPY ./poetry.lock /app/

RUN pip install --upgrade pip \
    && pip install poetry


RUN poetry install --no-root --only=main

COPY ./hfin /app/
