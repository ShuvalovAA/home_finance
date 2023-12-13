"""Хранилище коннекторов к базам данных."""
from contextlib import asynccontextmanager
from functools import partial
from typing import Optional

import aiopg
import aioredis
from fastapi_clickhouse.connector import connect
from fastapi_clickhouse.settings import from_env as ch_from_env
from fastapi_clickhouse.types import Connector as CHConnector
from fastapi_pg.settings import Settings as PGSettings
from fastapi_pg.settings import from_env as pg_from_env
from fastapi_pg.types import Connection
from fastapi_pg.types import Connector as PGConnector
from fastapi_redis.settings import Settings as RedisSettings
from fastapi_redis.settings import from_env as redis_from_env
from fastapi_redis.types import Connector as RedisConnector
from psycopg2.extras import DictCursor

from changeset.settings import APP_NAME

__all__ = [
    'Connectors'
]


class Connectors:
    """Класс коннекторов к базам данных, требуемых микросервису."""

    def __init__(
            self,
            partner_id: str,
            pg_connector: Optional[PGConnector] = None,
            ch_connector: Optional[CHConnector] = None,
            redis_connector: Optional[RedisConnector] = None
    ):
        self.partner_id = partner_id
        self.pg_connector = pg_connector
        self.ch_connector = ch_connector
        self.redis_connector = redis_connector

    async def _get_redis_connector(self) -> RedisConnector:
        settings: RedisSettings = redis_from_env(APP_NAME)
        pool = aioredis.from_url(
            settings.dsn,
            max_connections=settings.max_pool_size,
            socket_timeout=settings.timeout,
            encoding='utf-8',
            decode_responses=True,
        )
        return pool.client

    async def _get_ch_connector(self) -> CHConnector:
        settings = ch_from_env(APP_NAME)
        connector = partial(
            connect,
            url=settings.url,
            database=settings.database,
            user=settings.user,
            password=settings.password,
            timeout=settings.timeout,
        )
        return connector

    async def _get_pg_connector(self) -> PGConnector:
        settings: PGSettings = pg_from_env(APP_NAME)
        pool = await aiopg.create_pool(
            settings.dsn,
            minsize=settings.min_pool_size,
            maxsize=settings.max_pool_size,
            timeout=settings.timeout,
        )

        @asynccontextmanager
        async def connect() -> Connection:
            """Контекстный менеджер, осуществляющий подключение к PostgreSQL."""
            async with pool.acquire() as connection:
                async with connection.cursor(cursor_factory=DictCursor) as cursor:
                    yield cursor
        return connect

    async def build_connectors(self):
        """Собрать коннекторы в экземпляр класса."""
        self.pg_connector = await self._get_pg_connector()
        self.ch_connector = await self._get_ch_connector()
        self.redis_connector = await self._get_redis_connector()
