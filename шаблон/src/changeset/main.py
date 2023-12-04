"""Сервис миграции логов DML."""
import fastapi_pg as pg
import fastapi_clickhouse as clickhouse
import fastapi_redis as redis
from fastapi import FastAPI
from fastapi_application import ApplicationBuilder

from changeset.views import common as common_views
from changeset.settings import APP_NAME


def get_application() -> FastAPI:
    """Инициализировать приложение сервиса миграции DML логов."""
    builder = ApplicationBuilder(APP_NAME, description=__doc__)

    builder.apply(pg.register, APP_NAME)
    builder.apply(clickhouse.register, APP_NAME)
    builder.apply(redis.register, APP_NAME)

    common_views.register(builder)

    return builder.build()
