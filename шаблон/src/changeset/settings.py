"""Общие настройки микросервиса"""
# from celery import app
# from fastapi_redis import Connector
# # Celery
# app.conf.broker_transport_options = {'master_name': "cluster1"}
# app.conf.broker_url = 'redis://localhost:6379/0'
APP_NAME = 'changeset'
TIME_AFTER_LAST_PROCESS_MIN = 15
PART_COUNT = 50000