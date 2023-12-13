"""Вспомогательные утилиты сервиса."""
import datetime
import os
from typing import Dict, List

import jsonlines

from changeset.exceptions import DataNotFound, ThrottlingError
from changeset.settings import TIME_AFTER_LAST_PROCESS_MIN, TMP_DIR
from changeset.storage.managers.utils_manager import UtilsManager
from changeset.storage.query_builders.utils_query_builder import UtilsQueryBuilder

__all__ = [
    'СheckerThrottling',
    'SerialazerJSONL',
    'TmpDirCleaner'
]


class СheckerThrottling(UtilsQueryBuilder):
    """Класс чекера, отвечаюшего за проверку выполнения условий тротлинга."""

    def __init__(self, connectors):
        """Инициализация объекта чекера."""
        self.manager = UtilsManager(connectors=connectors)
        self.block_cache_key = f'process_for_{connectors.partner_id}'
        self.time_throttling = TIME_AFTER_LAST_PROCESS_MIN

    async def check(
            self,
            target_table: str,
            period_start: datetime.date,
            period_end: datetime.date
    ) -> bool:
        """Проверка условий тротлинга."""
        key_is_free = await self.manager.redis_manager.check_key_is_free(
            block_cache_key=self.block_cache_key
        )
        process_is_not = await self.manager.pg_manager.check_last_process(
            time_throttling=self.time_throttling
        )
        data_exists = await self.manager.ch_manager.check_data_exists(
            target_table=target_table,
            period_start=period_start,
            period_end=period_end
        )
        if not data_exists:
            raise DataNotFound
        process_allowed = all([key_is_free, process_is_not])
        if not process_allowed:
            raise ThrottlingError


class SerialazerJSONL:
    """Класс сериализатора JSONL."""

    def __init__(self, data: List[Dict], partner_id: int) -> str:
        self.data = data
        self.path = f'{TMP_DIR}/{partner_id}_datetime_{str(datetime.datetime.now())}.jsonl'

    async def to_serilize_in_file(self) -> str:
        """Сериализовать объект."""
        with jsonlines.open(self.path, 'w') as writer:
            writer.write_all(self.data)
        return self.path


class TmpDirCleaner:
    """Класс клинера, очищающего директорию от временных файлов."""

    def __init__(self, partner_id):
        self.partner_id = partner_id

    async def clean_dir_by_partner(self) -> None:
        """Удалить временные файлы по партнёру."""
        for file_name in os.listdir(TMP_DIR):
            if file_name.split('_')[0] == str(self.partner_id):
                os.remove(f'{TMP_DIR}/{file_name}')
