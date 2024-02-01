"""
'''
В папке /etc/nginx/sites-enabled создаем ссылку на файл mysite_nginx.conf, чтобы nginx увидел его:
sudo ln -s nginx.conf /etc/nginx/sites-enabled/
'''

-
Создадим и откроем файл по следующему пути:

sudo vim /etc/systemd/system/gunicorn.socket
В этот файл нужно поместить следующую информацию:

[Unit]
Description=Gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
-

sudo vim /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=alex
Group=alex
WorkingDirectory=/fixmypc_folder/fixmypc_project
ExecStart=/usr/local/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          fixmypc_project.wsgi:application

[Install]
WantedBy=multi-user.target
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')


# poetry run gunicorn --reload wsgi:application --bind 127.0.0.1:9393
application = get_wsgi_application()
