import os
from datetime import date
from celery import Celery
from fastapi import Depends
from changeset.settings import APP_NAME
from changeset.storage.connectors import ConnectorsStorage
from changeset.handlers.uploader_part import Uploader
from changeset import storage

celery = Celery(__name__)
redis_host = os.environ.get('CHANGESET_REDIS_HOST')
redis_port = os.environ.get('CHANGESET_REDIS_PORT')
redis_url = f'redis://{redis_host}:{redis_port}'
celery.conf.broker_url = redis_url
celery.conf.result_backend = redis_url



@celery.task()
async def upload_process_task(
        uploading_director_id: int,
        partner_id: int,
        target_table: str,
        period_start: date,
        period_end: date,
        connectors: ConnectorsStorage

) -> None:

    uploader = Uploader(
        uploading_director_id=uploading_director_id,
        partner_id=partner_id,
        target_table=target_table,
        period_start=period_start,
        period_end=period_end,
        connectors=connectors
    )
    await uploader.start_build_data()
