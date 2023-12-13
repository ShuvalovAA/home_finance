from datetime import date
from typing import Dict, List, Optional

from aiochclient.records import Record

from changeset.clients.yandex_s3_client import YandexS3
from changeset.exceptions import DataNotFound
from changeset.storage.query_builders.chief_query_bilders import ChiefQueryBuilder

__all__ = [
    'ChiefManager'
]


class ChiefManager:
    """Менеджер руководителя для взаимодействия с хранилищами."""

    def __init__(self, connectors):
        self.redis_manager = self.RedisManager(connector=connectors.redis_connector)
        self.pg_manager = self.PGManager(connector=connectors.pg_connector, partner_id=connectors.partner_id)
        self.ch_manager = self.CHManager(connector=connectors.ch_connector, partner_id=connectors.partner_id)
        self.yandex_storage_manager = self.YandexStorageManager(partner_id=connectors.partner_id)

    class RedisManager:
        """Менеджер выполнения запросов в Redis."""

        def __init__(self, connector):
            self.connector = connector

        async def delete_block_key(self, block_cache_key: str) -> None:
            """Удалить ключи блокировки в кэш."""
            async with self.connector() as client:
                await client.delete(block_cache_key)

    class CHManager:
        """Менеджер выполнения запросов в ClickHouse."""

        def __init__(self, connector, partner_id):
            self.partner_id = partner_id
            self.connector = connector
            self.query_builder = ChiefQueryBuilder(partner_id=self.partner_id)

        async def _transformation_data(self, data: List[Record]) -> List[Dict]:
            """Трансформировать данные в список словарей."""
            result_list = []
            for record in data:
                keys = [k for k in record.keys()]
                values = [v for v in record.values()]
                record_dict = dict(zip(keys, values))
                result_list.append(record_dict)
            return result_list

        async def get_data(
                self,
                limit: int,
                offset: int,
                target_table: str,
                period_start: date,
                period_end: date,
        ):
            """Получить данные из ClickHouse."""
            query = self.query_builder.build_query_ch_get_query_select_ch(
                limit=limit,
                offset=offset,
                target_table=target_table,
                period_start=period_start,
                period_end=period_end
            )

            async with self.connector() as client:
                all_rows = await client.fetch(query)
                if not all_rows:
                    raise DataNotFound
            data = await self._transformation_data(all_rows)
            return data

    class PGManager:
        """Менеджер выполнения запросов в PostgreSQL."""

        def __init__(self, connector, partner_id):
            self.connector = connector
            self.partner_id = partner_id
            self.query_builder = ChiefQueryBuilder(partner_id=self.partner_id)

        async def update_process_record(
                self,
                process_id: int,
                parts_count: int,
                status: int,
                msg_abort: Optional[str] = None
        ):
            """Обновить запись о состоянии процесса."""
            query = self.query_builder.build_query_pg_get_query_update_upload_record(
                process_id=process_id,
                parts_count=parts_count,
                status=status,
                msg_abort=msg_abort
            )
            async with self.connector() as client:
                await client.execute(query)

        async def get_upload_key_and_multipart_id(self, process_id: int) -> List[str]:
            """Вернуть ключ и id составной загрузки."""
            query = self.query_builder.build_query_get_upload_key_and_multipart_id(process_id=process_id)
            async with self.connector() as client:
                await client.execute(query)
                result = await client.fetchone()
            return result

        async def create_uploading_part_record(
                self,
                process_id: int,
                status: int,
                part_position: int
        ) -> int:
            """Создать запись о загружаемом фрагменте в БД."""
            query = self.query_builder.build_query_pg_get_query_insert_pg(
                process_id=process_id,
                status=status,
                part_position=part_position
            )
            async with self.connector() as client:
                await client.execute(query)
                result = await client.fetchone()
            return result[0]

        async def update_uploading_part_record(
                self,
                process_id: int,
                part_id: int,
                status: int,
                part_position: int,
                etag: str
        ):
            """Обновить запись о загружаемом фрагменте в БД."""
            query = self.query_builder.build_query_pg_get_query_update_part_record(
                process_id=process_id,
                part_id=part_id,
                status=status,
                part_position=part_position,
                etag=etag
            )
            async with self.connector() as client:
                await client.execute(query)

        async def increment_parts_count(self, parts_count: int, status: int, process_id: int):
            """Увеличить счётчик количества загружаемых фрагментов."""
            query = self.query_builder.build_query_pg_get_query_update_upload_record(
                process_id=process_id,
                status=status,
                parts_count=parts_count
            )
            async with self.connector() as client:
                await client.execute(query)

        async def get_all_parts_list(self, process_id: int) -> List[Dict[str, str]]:
            """Вернуть список словарей всех фрагментов с ETag и PartNumber."""
            query = self.query_builder.build_query_get_all_parts_list(process_id=process_id)
            async with self.connector() as client:
                await client.execute(query)
                result = await client.fetchall()
            result = {'Parts': [{'ETag': r[0], 'PartNumber': r[1]} for r in result]}
            return result

    class YandexStorageManager:
        """Менеджер выполнения запросов в Yandex Object Storage."""

        def __init__(self, partner_id):
            self.partner_id = partner_id
            self.proxy_client = YandexS3(partner_id=self.partner_id)

        async def write_part_in_storage(self, file_path, key, part_number, multipart_id):
            """Записать фрагмент на стораж."""
            return await self.proxy_client.upload_part(
                file_path=file_path,
                key=key,
                part_number=part_number,
                multipart_id=multipart_id
            )

        async def complete_process_on_storage(
            self,
            key: str,
            multipart_id: str,
            parts_list: List[Dict[str, str]]
        ):
            """Завершить процесс составной загрузки на YandexStorage."""
            return await self.proxy_client.complete_multipart_upload(
                key=key,
                multipart_id=multipart_id,
                parts_list=parts_list
            )

        async def abort_process_on_storage(
                self,
                key: str,
                multipart_id: str
        ):
            """Прервать процесс составной загрузки на YandexStorage."""
            return await self.proxy_client.abort_multipart_upload(
                key=key,
                multipart_id=multipart_id
            )

        async def get_url_on_file(self):
            """Получить ссылку на готовый файл многосоставной загрузки."""
            pass
