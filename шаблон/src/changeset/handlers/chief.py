from datetime import date
from typing import Optional

from changeset.exceptions import DataNotFound
from changeset.handlers.utils import SerialazerJSONL, TmpDirCleaner
from changeset.settings import PART_COUNT
from changeset.storage.connectors import Connectors
from changeset.storage.managers.chief_manager import ChiefManager

__all__ = [
    'Chief'
]


class Chief:
    """Класс руководителя составной загрузки."""

    class Statuses:
        """Статусы используемые руководителем."""

        DONE = 1
        IN_PROGRESS = 2
        IS_ABORTED = 3

    def __init__(
            self,
            upload_process_id: int,
            partner_id: int,
            target_table: str,
            period_start: date,
            period_end: date,
            connectors: Connectors,
    ):
        self.upload_process_id = upload_process_id
        self.partner_id = partner_id
        self.target_table = target_table
        self.period_start = period_start
        self.period_end = period_end
        self.connectors = connectors
        self.file_cleaner = TmpDirCleaner(partner_id=self.partner_id)
        self.block_key = f'process_for_{self.partner_id}'

        self.manager = ChiefManager(connectors=connectors)
        self.part_id = None
        self.data = None
        self.upload_key = None
        self.multipart_id = None
        self.part_position = 0
        self.offset = 0

    async def _clean_key_tmp(self) -> None:
        """Очистить ключ и директорию временных файлов."""
        await self.manager.redis_manager.delete_block_key(block_cache_key=self.block_key)
        await self.file_cleaner.clean_dir_by_partner()

    async def _abort(self, msg_abort: Optional[str] = None):
        """Прервать процесс составной загрузки."""
        await self.manager.pg_manager.update_process_record(
            process_id=self.upload_process_id,
            parts_count=0,
            status=self.Statuses.IS_ABORTED,
            msg_abort=msg_abort
        )
        await self.manager.yandex_storage_manager.abort_process_on_storage(
            key=self.upload_key,
            multipart_id=self.multipart_id
        )
        await self._clean_key_tmp()

    async def _complete(self):
        """Завершить загрузку."""
        await self.manager.yandex_storage_manager.complete_process_on_storage(
            key=self.upload_key,
            multipart_id=self.multipart_id,
            parts_list=await self._get_all_parts_list()
        )
        await self.manager.pg_manager.update_process_record(
            process_id=self.upload_process_id,
            parts_count=self.part_position,
            status=self.Statuses.DONE,
        )
        await self._clean_key_tmp()

    async def _get_all_parts_list(self):
        """Получить список словарей всех фрагментов с ETag и PartNumber."""
        return await self.manager.pg_manager.get_all_parts_list(
            process_id=self.upload_process_id
        )

    async def _get_upload_key_and_multipart_id(self):
        """Получить ключ и id по составной загрузке."""
        return await self.manager.pg_manager.get_upload_key_and_multipart_id(
            process_id=self.upload_process_id
        )

    async def start_build_data(self):
        """Начать запись фрагмента на стораж."""
        self.upload_key, self.multipart_id = await self._get_upload_key_and_multipart_id()
        while 1:
            try:

                self.data = await self.manager.ch_manager.get_data(
                    limit=PART_COUNT,
                    offset=self.offset,
                    target_table=self.target_table,
                    period_start=self.period_start,
                    period_end=self.period_end,
                )
                self.part_position += 1

            except DataNotFound:
                # Если первый же чанк пустой абортим загрузку.
                if self.part_position == 0:
                    await self._abort(msg_abort='data not found')
                    break

                await self._complete()
                break

            self.part_id = await self.manager.pg_manager.create_uploading_part_record(
                process_id=self.upload_process_id,
                status=self.Statuses.IN_PROGRESS,
                part_position=self.part_position
            )
            serializer = SerialazerJSONL(data=self.data, partner_id=self.partner_id)
            file_path = await serializer.to_serilize_in_file()
            try:
                part_etag = await self.manager.yandex_storage_manager.write_part_in_storage(
                    file_path=file_path,
                    part_number=self.part_position,
                    key=self.upload_key,
                    multipart_id=self.multipart_id
                )
            except Exception as e:
                await self._abort(msg_abort=e.__str__())
                raise e
            await self.manager.pg_manager.update_uploading_part_record(
                process_id=self.upload_process_id,
                part_id=self.part_id,
                status=self.Statuses.DONE,
                part_position=self.part_position,
                etag=part_etag
            )
            self.offset += PART_COUNT
            await self.manager.pg_manager.increment_parts_count(
                process_id=self.upload_process_id,
                parts_count=self.part_position,
                status=self.Statuses.IN_PROGRESS
            )
