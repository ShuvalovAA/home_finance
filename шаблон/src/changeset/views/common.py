"""Обработчики запросов управления мигратером."""
from fastapi import Depends, HTTPException
from fastapi_application import ApplicationBuilder

from changeset import storage
from changeset.exceptions import DataNotFound, PartnerOrUploadNotFound, ThrottlingError
from changeset.handlers.starter import Starter
from changeset.handlers.utils import СheckerThrottling
from changeset.settings import APP_NAME
from changeset.storage.common import StorageCommon
from changeset.storage.connectors import Connectors
from changeset.tasks.common import upload_process_task
from changeset.views.models import (
    GetUploadingStatusRequest,
    GetUploadingStatusResponse,
    GetUrlChangesetFileRequest,
    GetUrlChangesetFileResponse,
    StartMigrateChangesetRequest,
    StartMigrateChangesetResponse,
)

__all__ = [
    'GetUrlChangesetFileResponse',
    'GetUrlChangesetFileRequest',
    'StartMigrateChangesetResponse',
    'StartMigrateChangesetRequest',
    'GetUploadingStatusRequest',
    'GetUploadingStatusResponse'
]


async def start_migrate_changeset(
    request: StartMigrateChangesetRequest,
    connectors: Connectors = Depends(storage.get_connectors(APP_NAME))
) -> StartMigrateChangesetResponse:
    """Запрос начала составной загрузки DML.

    *Выполнение доступно, если с момента последнего запроса прошло 15 минут
    и в процессе нет ни одной загрузки. Иначе будет получен код 429.

    - target_table_name: имя таблицы, по которой нужны логи DML;
    - period_start: дата начала периода для поиска логов;
    - period_end: дата окончания периода для поиска логов.

    Если запрос успешен, то в теле ответа вернётся uploading_id,
    по которому можно запросить статус процесса загрузки
    методом getUploadingStatus.
    """
    connectors.partner_id = connectors.partner_id
    checker = СheckerThrottling(connectors=connectors)
    try:
        await checker.check(
            target_table=request.target_table_name,
            period_start=request.period_start,
            period_end=request.period_end
        )
    except ThrottlingError as error:
        raise HTTPException(status_code=429, detail=error.message)
    except DataNotFound as error:
        raise HTTPException(status_code=404, detail=error.message)

    starter = Starter(
        partner_id=connectors.partner_id,
        target_table=request.target_table_name,
        period_start=request.period_start,
        period_end=request.period_end,
        connectors=connectors
    )
    try:
        await starter.initialize_upload()
    except ThrottlingError as error:
        raise HTTPException(status_code=429, detail=error.message)

    upload_process_task.delay(
        upload_process_id=starter.upload_process_id,
        partner_id=starter.partner_id,
        target_table=request.target_table_name,
        period_start=request.period_start,
        period_end=request.period_end,
    )

    return StartMigrateChangesetResponse(ok=True, uploading_id=starter.upload_process_id)


async def get_uploading_status(
    request: GetUploadingStatusRequest,
    connectors: Connectors = Depends(storage.get_connectors(APP_NAME))
) -> GetUploadingStatusResponse:
    """Запрос получения статуса процесса загрузки логов DML.

    Варианты ответа по статусам:
    - 1: Загрузка заверешена;
    - 2: Загрузка в процессе;
    - 3: Загрузка прервана по техническим причинам.

    Если статус 1, то файл ставится в очередь на формирование.
    Используйте getUrlChangesetFile для проверки готовности файла и получения url.
    """
    storage_common = StorageCommon(
        connectors=connectors
    )
    try:
        status = await storage_common.get_uploading_status(uploading_id=request.uploading_id)
    except PartnerOrUploadNotFound as error:
        raise HTTPException(status_code=404, detail=error.message)

    return GetUploadingStatusResponse(ok=True, uploading_status=status, description=None)


def register(builder: ApplicationBuilder) -> None:
    """Зарегистрировать обработчики запросов."""
    builder.register_endpoint(
        'api/v1/startMigrateChangeset',
        start_migrate_changeset,
        response_model=StartMigrateChangesetResponse,
        responses=StartMigrateChangesetResponse.get_responses(),
        tags=['v1'],
    )

    builder.register_endpoint(
        'api/v1/getUploadingStatus',
        get_uploading_status,
        response_model=GetUploadingStatusResponse,
        responses=GetUploadingStatusResponse.get_responses(),
        tags=['v1'],
    )
