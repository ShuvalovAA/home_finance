from datetime import date
from changeset.settings import PART_COUNT
from changeset.handlers.utils import SerialazerJSONL
from changeset.handlers.uploading_director import UploadingDirector
from changeset.storage.managers.uploader_part_manager import UploaderManager
from changeset.storage.connectors import ConnectorsStorage
from changeset.exceptions import DataNotFound


class Uploader:
    """Класс фрагмента составной загрузки."""
    class Statuses:
        DONE = 1
        IN_PROGRESS = 2
        IS_ABORTED = 3

    def __init__(
            self,
            uploading_director_id: int,
            partner_id: int,
            target_table: str,
            period_start: date,
            period_end: date,
            connectors: ConnectorsStorage,
    ):
        self.uploading_director_id = uploading_director_id
        self.partner_id = partner_id
        self.target_table = target_table
        self.period_start = period_start
        self.period_end = period_end
        self.connectors = connectors

        self.manager = UploaderManager(connectors=connectors)
        self.part_id = None
        self.data = None
        self.part_position = 1
        self.offset = 0

    async def start_build_data(self):
        """Начать запись фрагмента на стораж."""
        while 1:
            self.part_id = await self.manager.pg_manager.create_uploading_part_record(
                process_id=self.uploading_director_id,
                status=self.Statuses.IN_PROGRESS,
                part_position=self.part_position
            )

            #try:
            self.data = await self.manager.ch_manager.get_data(
                limit=PART_COUNT,
                offset=self.offset,
                target_table=self.target_table,
                period_start=self.period_start,
                period_end=self.period_end,
            )
            #except DataNotFound:
            serializer = SerialazerJSONL(data=self.data)
            file_path = await serializer.to_serilize_in_file()
            await self.manager.yandex_storage_manager.write_part_in_storage(file_path)

            await self.manager.pg_manager.update_uploading_part_record(
                process_id=self.uploading_director_id,
                part_id=self.part_id,
                status=self.Statuses.DONE
            )
            self.part_position += 1
            self.offset += PART_COUNT

            await self.manager.pg_manager.increment_parts_count(
                process_id=self.uploading_director_id,
                parts_count=self.parts_count,
                status=self.Statuses.IN_PROGRESS
            )