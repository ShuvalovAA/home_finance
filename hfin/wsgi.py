"""
WSGI config for hfin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

# poetry run uvicorn --reload wsgi:application --host 0.0.0.0 --port 9393
application = get_wsgi_application()
