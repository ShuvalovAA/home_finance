"""Общие настройки микросервиса."""

import os

# APP settings
APP_NAME = os.environ.get('APP_NAME')
TMP_DIR = os.environ.get('TMP_DIR')

# Throttling settings
TIME_AFTER_LAST_PROCESS_MIN = 15

# Upload settings
PART_COUNT = 50000

# YandexS3 settings
BUCKET_NAME = os.environ.get('BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION_NAME = 'ru-central1'
SERVICE_NAME = 's3'
ENDPOINT_URL = 'https://storage.yandexcloud.net'

# Redis settings
REDIS_HOST = os.environ.get('CHANGESET_REDIS_HOST')
REDIS_PORT = os.environ.get('CHANGESET_REDIS_PORT')
redis_url = f'redis://{REDIS_HOST}:{REDIS_PORT}'

# Celery settings
INCLUDE_TASKS_MODULE = [
    'changeset.tasks.common'
]
os.environ['CELERY_RESULT_BACKEND'] = redis_url
os.environ['CELERY_BROKER_URL'] = redis_url
