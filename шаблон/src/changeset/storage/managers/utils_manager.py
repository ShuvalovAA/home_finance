
from changeset.storage.query_bilders import UtilsQueryBuilder


class UtilsManager:
    def __init__(self, connectors):
        self.redis_manager = self.RedisManager(connector=connectors.redis_connector)
        self.pg_manager = self.PGManager(connector=connectors.pg_connector, partner_id=connectors.partner_id)

    class RedisManager:
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
        def __init__(self, connector, partner_id):
            self.connector = connector
            self.partner_id = partner_id

        async def check_last_process(self, time_throttling: int) -> bool:
            """Проверяем прошло ли 15 минут с последней выгрузки."""
            query = self.build_query_check_last_partner_upload_process(time_throttling=time_throttling)
            async with self.connector() as client:
                process_exists = await client.execute(query)
            if process_exists:
                return False
            return True


