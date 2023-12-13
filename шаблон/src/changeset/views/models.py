"""Модели общей схемы запросов и ответов."""
from datetime import date

from pydantic import BaseModel, Field

__all__ = [
    'StartMigrateChangesetRequest',
    'StartMigrateChangesetResponse',
    'GetUrlChangesetFileRequest',
    'GetUrlChangesetFileResponse',
    'GetUploadingStatusRequest',
    'GetUploadingStatusResponse',
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

    uploading_id: int = Field(description='ID инициализированной загрузки.', nullable=False)

    @staticmethod
    def get_responses() -> dict:
        """Возможные коды ответов."""
        return {
            '200': {'description': 'Операция успешно запущена.'},
            '404': {'description': 'Данных за указанный период нет.'},
            '429': {'description': 'Превышен лимит запросов.'}
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


class GetUploadingStatusRequest(BaseModel):
    """Запрос статуса процесса загрузки логов DML."""

    uploading_id: int = Field(description='ID инициализированной загрузки.', nullable=False)


class GetUploadingStatusResponse(DefaultResponse):
    """Ответ получения сстатуса процесса загрузки логов DML."""

    uploading_status: int

    @staticmethod
    def get_responses() -> dict:
        """Возможные коды ответов."""
        return {
            '200': {'description': 'Операция успешно завершена.'},
            '404': {'description': 'Данные по партнёру и по идентификатору загрузки не найдены.'},
        }
