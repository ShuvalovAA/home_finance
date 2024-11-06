"""
ASGI config for hfin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django
import sentry_sdk
from root import settings
from sentry_sdk.integrations.django import DjangoIntegration

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

# poetry run python manage.py runserver 127.0.0.1:9393 < ---- рабочий
# poetry run uvicorn --reload asgi:application --host 127.0.0.1 --port 9393 < ---- рабочий

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[
        DjangoIntegration(
            transaction_style='url',
            middleware_spans=True,
            signals_spans=True,
            signals_denylist=[
                django.db.models.signals.pre_init,
                django.db.models.signals.post_init,
            ],
            cache_spans=False,
            http_methods_to_capture=("GET",),
        ),
    ],
)

application = get_asgi_application()
