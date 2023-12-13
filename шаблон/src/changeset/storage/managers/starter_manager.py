from datetime import date

from changeset.clients.yandex_s3_client import YandexS3
from changeset.storage.query_builders.starter_query_builder import StarterQueryBuilder

__all__ = [
    'StarterManager'
]


class StarterManager:
    """Менеджер стартера для взаимодействия с хранилищами."""

    def __init__(self, connectors):
        self.redis_manager = self.RedisManager(connector=connectors.redis_connector)
        self.pg_manager = self.PGManager(connector=connectors.pg_connector, partner_id=connectors.partner_id)
        self.yandex_storage_manager = self.YandexStorageManager(partner_id=connectors.partner_id)

    class RedisManager:
        """Менеджер выполнения запросов в Redis."""

        def __init__(self, connector):
            self.connector = connector

        async def check_key_is_free(self, block_cache_key: str) -> bool:
            """Проверить есть ли в кэше задача в работе по ключу."""
            async with self.connector() as client:
                key_exists = await client.exists(block_cache_key)
            if key_exists:
                return False
            return True

        async def set_block_key(self, block_cache_key: str) -> None:
            """Установить ключи блокировки в кэш."""
            # проверить что ключ свободен
            async with self.connector() as client:
                await client.set(block_cache_key, value=1)

        async def delete_block_key(self, block_cache_key: str) -> None:
            """Удалить ключи блокировки в кэш."""
            async with self.connector() as client:
                await client.delete(block_cache_key)

    class PGManager:
        """Менеджер выполнения запросов в PostgreSQL."""

        def __init__(self, connector, partner_id):
            self.connector = connector
            self.query_builder = StarterQueryBuilder(partner_id=partner_id)

        async def create_process_record(
                self,
                partner_id: int,
                status: int,
                target_table: str,
                period_start: date,
                period_end: date,
                storage_key: str,
                multipart_id: str
        ) -> int:
            """Создать записи процесса в базе данных."""
            # проверить записи нет
            query = self.query_builder.build_query_pg_get_query_insert(
                status=status,
                target_table=target_table,
                period_start=period_start,
                period_end=period_end,
                storage_key=storage_key,
                multipart_id=multipart_id
            )
            async with self.connector() as client:
                await client.execute(query)
                result = await client.fetchone()
            return result[0]

    class YandexStorageManager:
        """Менеджер выполнения запросов в Yandex Object Storage."""

        def __init__(self, partner_id):
            self.partner_id = partner_id
            self.proxy_client = YandexS3(partner_id=partner_id)

        async def start_process_on_storage(self, key: str):
            """Начать процесс составной загрузки на YandexStorage."""
            return await self.proxy_client.start_multipart_upload(key=key)
