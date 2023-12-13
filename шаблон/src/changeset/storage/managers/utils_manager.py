import datetime

from changeset.storage.query_builders.utils_query_builder import UtilsQueryBuilder

__all__ = [
    'UtilsManager'
]


class UtilsManager:
    """Менеджер взаимодействия с хранилищами для утилит микросервиса."""

    def __init__(self, connectors):
        self.partner_id = connectors.partner_id
        self.redis_manager = self.RedisManager(connector=connectors.redis_connector)
        self.pg_manager = self.PGManager(connector=connectors.pg_connector, partner_id=connectors.partner_id)
        self.ch_manager = self.CHManager(connector=connectors.ch_connector, partner_id=connectors.partner_id)

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

    class PGManager(UtilsQueryBuilder):
        """Менеджер выполнения запросов в PostgreSQL."""

        def __init__(self, connector, partner_id):
            self.connector = connector
            self.partner_id = partner_id

        async def check_last_process(self, time_throttling: int) -> bool:
            """Проверяем прошло ли 15 минут с последней выгрузки."""
            query = self.build_query_check_last_partner_upload_process(time_throttling=time_throttling)
            async with self.connector() as client:
                await client.execute(query)
                result = await client.fetchone()
            if result[0]:
                return False
            return True

    class CHManager(UtilsQueryBuilder):
        """Менеджер выполнения запросов в ClickHouse."""

        def __init__(self, connector, partner_id):
            self.connector = connector
            self.partner_id = partner_id

        async def check_data_exists(
                self,
                target_table: str,
                period_start: datetime.date,
                period_end: datetime.date
        ) -> bool:
            """Проверить есть ли данные за указанный период."""
            query = self.build_query_check_data_exists(
                target_table=target_table,
                period_start=period_start,
                period_end=period_end
            )
            async with self.connector() as client:
                data_exists = await client.fetchone(query)
            if data_exists[0]:
                return True
            return False
