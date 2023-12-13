"""Хранилище атрибутов пользователей общей схемы для FastAPI."""

from typing import Callable, Optional

from fastapi import Depends, Security
from fastapi_clickhouse import Connector as CHConnector
from fastapi_clickhouse import get_client as get_client_ch
from fastapi_pg import Connector as PGConnector
from fastapi_pg import get_client as get_client_pg
from fastapi_redis import Connector as RedisConnector
from fastapi_redis import get_client as get_client_redis
from fastapi_security_headers import get_partner_id

from changeset.storage.connectors import Connectors

__all__ = [
    'get_connectors',
]


def get_connectors(name: Optional[str] = None) -> Callable:
    """Создать резолвер для получения хранилища через именованное соедениение.

    Принимает следующие аргументы:
        name: Имя соединения (опционально).
    """

    def getter(
        partner_id: int = Security(get_partner_id),
        pg_connector: PGConnector = Depends(get_client_pg(name)),
        ch_connector: CHConnector = Depends(get_client_ch(name)),
        redis_connector: RedisConnector = Depends(get_client_redis(name))
    ) -> Connectors:
        """Создать хранилище пользовательских атрибутов общей схемы."""
        return Connectors(
            pg_connector=pg_connector,
            ch_connector=ch_connector,
            redis_connector=redis_connector,
            partner_id=partner_id
        )

    return getter
