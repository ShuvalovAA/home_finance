from datetime import date
from changeset.storage.query_bilders import UploadingDirectorQueryBuilder


class UploadingDirectorManager:
    def __init__(self, connectors):
        self.redis_manager = self.RedisManager(connector=connectors.redis_connector)
        self.pg_manager = self.PGManager(connector=connectors.pg_connector, partner_id=connectors.partner_id)
        self.yandex_storage_manager = self.YandexStorageManager()

    class RedisManager:
        def __init__(self, connector):
            self.connector = connector

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
        def __init__(self, connector, partner_id):
            self.connector = connector
            self.query_builder = UploadingDirectorQueryBuilder(partner_id=partner_id)

        async def create_process_record(
                self,
                partner_id: int,
                status: int,
                target_table: str,
                period_start: date,
                period_end: date,
        ) -> int:
            """Создать записи процесса в базе данных."""
            # проверить записи нет
            query = self.query_builder.build_query_pg_get_query_insert(
                partner_id=partner_id,
                status=status,
                target_table=target_table,
                period_start=period_start,
                period_end=period_end
            )
            async with self.connector() as client:
                await client.execute(query)
                result = await client.fetchone()
            return result[0]

        async def update_process_record(self):
            """Обновить запись о состоянии процесса."""
            query = self.build_query_get_query_update()
            async with self.pg_conn() as client:
                await client.execute(query)

    class YandexStorageManager:
        def __init__(self):
            pass

        async def start_process_on_storage(self):
            """Начать процесс составной загрузки на YandexStorage."""
            pass

        async def abort_process_on_storage(self):
            """Прервать процесс составной загрузки на YandexStorage."""
            pass

        async def complete_process_on_storage(self):
            """Завершить процесс составной загрузки на YandexStorage."""
            pass

        async def get_url_on_file(self):
            """Получить ссылку на готовый файл многосоставной загрузки."""
            pass