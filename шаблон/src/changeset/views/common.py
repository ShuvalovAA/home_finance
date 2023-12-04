"""Обработчики запросов управления мигратером."""
from fastapi import Depends
from fastapi_application import ApplicationBuilder
from changeset import storage
from changeset.settings import APP_NAME

from changeset.views.models import (
    GetUrlChangesetFileRequest,
    GetUrlChangesetFileResponse,
    StartMigrateChangesetRequest,
    StartMigrateChangesetResponse,
)

from changeset.storage.connectors import ConnectorsStorage
from changeset.handlers.utils import СheckerThrottling
from changeset.exceptions import ThrottlingError
from changeset.handlers.uploading_director import UploadingDirector
from changeset.handlers.tasks import upload_process_task

__all__ = [
    'GetUrlChangesetFileResponse',
    'GetUrlChangesetFileRequest',
    'StartMigrateChangesetResponse',
    'StartMigrateChangesetRequest'
]


async def start_migrate_changeset(
    request: StartMigrateChangesetRequest,
    connectors_storage: ConnectorsStorage = Depends(storage.get_connectors_storage(APP_NAME))
) -> StartMigrateChangesetResponse:
    """Запрос начала составной загрузки DML."""
    checker = СheckerThrottling(connectors=connectors_storage)
    process_is_allowed = await checker.check()
    if not process_is_allowed:
        raise ThrottlingError
    director = UploadingDirector(
        partner_id=connectors_storage.partner_id,
        target_table=request.target_table_name,
        period_start=request.period_start,
        period_end=request.period_end,
        connectors=connectors_storage
    )
    await director.initialize()
    task = await upload_process_task(
        uploading_director_id=director.id,
        partner_id=director.partner_id,
        target_table=director.target_table,
        period_start=director.period_start,
        period_end=director.period_end,
        connectors=connectors_storage
    )
    #
    print(f'ok: ["task_id": {task.id}]')

    return StartMigrateChangesetResponse(ok=True)


async def get_url_changeset_file(
    request: GetUrlChangesetFileRequest,
) -> GetUrlChangesetFileResponse:
    """Запрос получения url на файл с логами DML."""
    return GetUrlChangesetFileResponse(ok=True)


def register(builder: ApplicationBuilder) -> None:
    """Зарегистрировать обработчики запросов."""
    builder.register_endpoint(
        'api/v1/startMigrateChangeset',
        start_migrate_changeset,
        response_model=StartMigrateChangesetResponse,
        tags=['v1'],
    )
    builder.register_endpoint(
        'api/v1/getUrlChangesetFile',
        get_url_changeset_file,
        response_model=GetUrlChangesetFileResponse,
        tags=['v1'],
    )
