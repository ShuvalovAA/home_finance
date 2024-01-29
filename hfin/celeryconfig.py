import os
# from celery.schedules import crontab
from datetime import timedelta
'''
export HFIN_REDIS_PORT=6379
export HFIN_REDIS_HOST=localhost
'''

REDIS_HOST: str = os.environ.get('HFIN_REDIS_HOST')
REDIS_PORT: str = os.environ.get('HFIN_REDIS_PORT')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

redis_url: str = f'redis://{REDIS_HOST}:{REDIS_PORT}'

INCLUDE_TASKS_MODULE = [
    'tasks.common'
]
INCLUDE_PERIODIC_TASKS = {
    'check_getting_income': {
        'task': 'check_getting_income',
        'schedule': timedelta(seconds=1)
    },
    'check_expired_subscribies': {
        'task': 'check_expired_subscribies',
        'schedule': timedelta(seconds=1)
    },
    'check_expiring_subscribies': {
        'task': 'check_expiring_subscribies',
        'schedule': timedelta(seconds=1)
    },
}

#    Broker settings.
broker_url = redis_url

# Using the database to store task state and results.
result_backend = redis_url

# delay tasks
include = INCLUDE_TASKS_MODULE

# beat tasks
beat_schedule = INCLUDE_PERIODIC_TASKS
