from datetime import date
from changeset.storage.connectors import ConnectorsStorage
from changeset.storage.managers.uploading_director_manager import UploadingDirectorManager


class UploadingDirector:
    """Класс, отвечающий за многосоставную загрузку."""
    class Statuses:
        DONE = 1
        IN_PROGRESS = 2
        IS_ABORTED = 3

    def __init__(
            self,
            partner_id: int,
            target_table: str,
            period_start: date,
            period_end: date,
            connectors: ConnectorsStorage,
    ):
        self.partner_id = partner_id
        self.target_table = target_table
        self.period_start = period_start
        self.period_end = period_end
        self.connectors = connectors
        self.id = None
        self.block_key = f'process_for_{self.partner_id}'

        self.manager = UploadingDirectorManager(
            connectors=connectors
        )

    async def _check_sequence_part(self):
        """Проверка последовательности фрагментов составной загрузки."""
        pass

    async def _abort_process(self):
        """Прервать процесс составной загрузки."""
        self.status = self.Statuses.IS_ABORTED
        await self.manager.update_process_record()
        await self.manager.abort_process_on_storage()
        await self.manager.delete_block_key()

    async def _complete_process(self):
        """Прервать процесс составной загрузки."""
        await self._check_sequence_part()  # может быть ошибка
        self.status = self.Statuses.DONE
        await self.manager.update_process_record()
        await self.manager.complete_process_on_storage()
        await self.manager.delete_block_key()

    async def initialize(self):
        """Инициализировать многосоставную загрузку."""
        # try:
        await self.manager.redis_manager.set_block_key(block_cache_key=self.block_key)
        await self.manager.yandex_storage_manager.start_process_on_storage()
        self.id = await self.manager.pg_manager.create_process_record(
            partner_id=self.partner_id,
            status=self.Statuses.IN_PROGRESS,
            target_table=self.target_table,
            period_start=self.period_start,
            period_end=self.period_end,
        )
        # except Exception as e:
        #     await self._abort_process()
        #     print(e)
