from datetime import date

from asgiref.sync import async_to_sync

from celery_app import CELERY_APP
from changeset.handlers.chief import Chief
from changeset.storage.connectors import Connectors


async def _start_upload_process(
        upload_process_id: int,
        partner_id: int,
        target_table: str,
        period_start: date,
        period_end: date
) -> None:
    connectors = Connectors(partner_id=partner_id)
    await connectors.build_connectors()
    uploader = Chief(
        upload_process_id=upload_process_id,
        partner_id=partner_id,
        target_table=target_table,
        period_start=period_start,
        period_end=period_end,
        connectors=connectors
    )
    await uploader.start_build_data()


@CELERY_APP.task(name='upload_process_task')
def upload_process_task(
        upload_process_id: int,
        partner_id: int,
        target_table: str,
        period_start: date,
        period_end: date
) -> None:
    """Таска отвечает за запуск процесса загрузки."""
    async_to_sync(_start_upload_process)(
        upload_process_id=upload_process_id,
        partner_id=partner_id,
        target_table=target_table,
        period_start=period_start,
        period_end=period_end
    )
