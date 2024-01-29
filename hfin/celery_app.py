import os

from celery import Celery
from celery.schedules import crontab


__all__ = [
    'CELERY_APP'
]


def get_celery_app():
    """Вернуть экземпляр celery.

    Метод возвращает экземпляр Celery для обработки отложенных и периодических задач.
    - команда запуска воркера: celery -A celery_app.CELERY_APP worker --loglevel=INFO
    - команда запуска планироващика : celery -A celery_app.CELERY_APP beat --loglevel=INFO
    """

    celery = Celery(
        'hfin',
    )
    celery.conf.timezone = 'UTC'
    default_config = 'celeryconfig'
    celery.config_from_object(default_config)
    return celery


CELERY_APP = get_celery_app()
