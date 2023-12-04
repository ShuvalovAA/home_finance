"""Хранилище атрибутов пользователей общей схемы для FastAPI."""

from fastapi import Depends,Security
from typing import Callable, Optional
from fastapi_security_headers import get_partner_id
from fastapi_pg import Connector as PGConnector, get_client as get_client_pg
from fastapi_clickhouse import Connector as CHConnector, get_client as get_client_ch
from fastapi_redis import Connector as RedisConnector, get_client as get_client_redis

from changeset.storage.connectors import ConnectorsStorage


__all__ = [
    'ConnectorsStorage',
    'get_connectors_storage',
]


def get_connectors_storage(name: Optional[str] = None) -> Callable:
    """Создать резолвер для получения хранилища через именованное соедениение.

    Принимает следующие аргументы:
        name: Имя соединения (опционально).
    """

    def getter(
        partner_id: int = Security(get_partner_id),
        pg_connector: PGConnector = Depends(get_client_pg(name)),
        ch_connector: CHConnector = Depends(get_client_ch(name)),
        redis_connector: RedisConnector = Depends(get_client_redis(name))
    ) -> ConnectorsStorage:
        """Создать хранилище пользовательских атрибутов общей схемы."""
        return ConnectorsStorage(
            pg_connector=pg_connector,
            ch_connector=ch_connector,
            redis_connector=redis_connector,
            partner_id=partner_id
        )

    return getter

