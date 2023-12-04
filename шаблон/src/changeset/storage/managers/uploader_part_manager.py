from typing import List, Dict
from aiochclient.records import Record
from datetime import date
from changeset.storage.query_bilders import UploaderQueryBuilder, UploadingDirectorQueryBuilder
from changeset.exceptions import DataNotFound


class UploaderManager:
    def __init__(self, connectors):
        self.pg_manager = self.PGManager(connector=connectors.pg_connector, partner_id=connectors.partner_id)
        self.ch_manager = self.CHManager(connector=connectors.ch_connector, partner_id=connectors.partner_id)
        self.yandex_storage_manager = self.YandexStorageManager(partner_id=connectors.partner_id)

    class CHManager:
        def __init__(self, connector, partner_id):
            self.connector = connector
            self.query_builder = UploaderQueryBuilder(partner_id=partner_id)

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
        def __init__(self, connector, partner_id):
            self.connector = connector
            self.query_builder = UploaderQueryBuilder(partner_id=partner_id)
            self.query_builder_director = UploadingDirectorQueryBuilder(partner_id=partner_id)

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
                status: int
            ):
            """Обновить запись о загружаемом фрагменте в БД."""
            query = self.query_builder.build_query_pg_get_query_update_pg(
                process_id=process_id,
                part_id=part_id,
                status=status
            )
            async with self.connector() as client:
                await client.execute(query)

        async def increment_parts_count(self, parts_count: int, status: int, process_id: int):
            """Увеличить счётчик количества загружаемых фрагментов."""
            query = self.query_builder_director.build_query_pg_get_query_update(
                process_id=process_id,
                status=status,
                parts_count=parts_count
            )
            self.parts_count += 1
            await self._update_process_record()

    class YandexStorageManager:
        def __init__(self, partner_id):
            self.partner_id = partner_id

        async def write_part_in_storage(self, data):
            """Записать фрагмент на стораж."""
            pass