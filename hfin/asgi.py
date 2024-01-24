"""
ASGI config for hfin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

# poetry run python manage.py runserver 127.0.0.1:9393 < ---- рабочий
# poetry run uvicorn --reload asgi:application --host 127.0.0.1 --port 9393 < ---- рабочий

application = get_asgi_application()
