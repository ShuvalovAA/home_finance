FROM python:3.9-alpine

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1

COPY . .

RUN apk add --update \
    gcc libc-dev linux-headers postgresql-dev && \
    pip install --no-cache-dir -r requirements.txt

#--no-cache --virtual .tmp-build-deps 