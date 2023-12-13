from celery import Celery

from changeset.settings import INCLUDE_TASKS_MODULE

__all__ = [
    'CELERY_APP'
]


def get_celery_app():
    """Вернуть эземпляр celery.

    Метод возвращает экземпляр Celery для обработки отложенных и периодических задач.
    - команда запуска воркера: celery -A celery_app.CELERY_APP worker --loglevel=INFO
    """
    celery = Celery(
        'changeset',
        include=INCLUDE_TASKS_MODULE
    )
    return celery


CELERY_APP = get_celery_app()
