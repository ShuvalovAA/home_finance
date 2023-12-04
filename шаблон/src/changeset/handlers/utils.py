"""Вспомогательные утилиты сервиса."""
import jsonlines
from datetime import datetime
from typing import List, Dict
from changeset.storage.query_bilders import UtilsQueryBuilder
from changeset.settings import TIME_AFTER_LAST_PROCESS_MIN
from changeset.storage.managers.utils_manager import UtilsManager


class СheckerThrottling(UtilsQueryBuilder):
    """Класс чекера, отвечаюшего за проверку выполнения условий тротлинга."""
    def __init__(self, connectors):
        """Инициализация объекта чекера."""
        self.manager = UtilsManager(connectors=connectors)
        self.block_cache_key = f'process_for_{connectors.partner_id}'
        self.time_throttling = TIME_AFTER_LAST_PROCESS_MIN

    async def check(self) -> bool:
        """Проверка условий тротлинга."""
        key_is_free = await self.manager.redis_manager.check_key_is_free(block_cache_key=self.block_cache_key)
        process_is_not = await self.manager.pg_manager.check_last_process(time_throttling=self.time_throttling)
        process_allowed = all([key_is_free, process_is_not])
        if process_allowed:
            return True
        return False


class SerialazerJSONL:
    """Класс сериализатора JSONL"""
    def __init__(self, data: List[Dict], partner_id,):
        self.data = data
        self.dir_tmp = '/home/shuva/Загрузки/'
        self.partner_id

        self.path = self.dir_tmp + self.partner_id +f'_datetime_{str(datetime.now())}'

    async def to_serilize_in_file(self) -> str:
        """Сериализовать объект"""

        with jsonlines.open(self.path, 'w') as writer:
            writer.write_all(self.data)

        return self.path



