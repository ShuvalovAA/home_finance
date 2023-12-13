from datetime import date

from changeset.exceptions import ThrottlingError
from changeset.storage.connectors import Connectors
from changeset.storage.managers.starter_manager import StarterManager

__all__ = [
    'Starter'
]


class Starter:
    """Класс, отвечающий за инициализацию многосоставной загрузки."""

    class Statuses:
        """Статусы, используемые стартером."""

        IN_PROGRESS = 2

    def __init__(
            self,
            partner_id: int,
            target_table: str,
            period_start: date,
            period_end: date,
            connectors: Connectors,
    ):
        self.partner_id = partner_id
        self.target_table = target_table
        self.period_start = period_start
        self.period_end = period_end
        self.connectors = connectors
        self.upload_process_id = None
        self.block_key = f'process_for_{self.partner_id}'
        self.manager = StarterManager(
            connectors=connectors
        )

    async def _get_key_for_storage(self):
        key = '_'.join([
            str(self.partner_id),
            self.target_table,
            str(self.period_start),
            str(self.period_end)
        ])
        return key

    async def initialize_upload(self):
        """Инициализировать загрузку."""
        key_is_free = await self.manager.redis_manager.check_key_is_free(block_cache_key=self.block_key)
        if not key_is_free:
            raise ThrottlingError
        await self.manager.redis_manager.set_block_key(block_cache_key=self.block_key)
        key = await self._get_key_for_storage()
        storage_key, storage_upload_id = await self.manager.yandex_storage_manager.start_process_on_storage(
            key=key
        )
        self.upload_process_id = await self.manager.pg_manager.create_process_record(
            partner_id=self.partner_id,
            status=self.Statuses.IN_PROGRESS,
            target_table=self.target_table,
            period_start=self.period_start,
            period_end=self.period_end,
            storage_key=storage_key,
            multipart_id=storage_upload_id
        )
