"""Модели общей схемы запросов и ответов."""
from datetime import date

from pydantic import BaseModel, Field

__all__ = [
    'StartMigrateChangesetRequest',
    'StartMigrateChangesetResponse',
    'GetUrlChangesetFileRequest',
    'GetUrlChangesetFileResponse',
    'DefaultResponse'
]


class DefaultResponse(BaseModel):
    """Стандартный ответ на запрос."""

    ok: bool = Field(
        description='Операция успешно завершена.'
    )


class StartMigrateChangesetRequest(BaseModel):
    """Запрос запуска сборки DML."""
    target_table_name: str = Field(description='Наименование целевой таблицы.', nullable=False)
    period_start: date = Field(description='Начало периода логов DML.', nullable=False)
    period_end: date = Field(description='Конец периода логов DML.', nullable=False)


class StartMigrateChangesetResponse(DefaultResponse):
    """Ответ запуска сборки логов DML."""

    @staticmethod
    def get_responses() -> dict:
        """Возможные коды ответов."""
        return {
            '200': {'description': 'Операция успешно запущена.'}
        }


class GetUrlChangesetFileRequest(BaseModel):
    """Запрос получения ссылки на файл с логами DML."""


class GetUrlChangesetFileResponse(DefaultResponse):
    """Ответ получения ссылки на файл."""

    @staticmethod
    def get_responses() -> dict:
        """Возможные коды ответов."""
        return {
            '200': {'description': 'Операция успешно завершена.'},
            '404': {'description': 'Не удалось найти ссылку на файл по составной загрузке.'},
        }
