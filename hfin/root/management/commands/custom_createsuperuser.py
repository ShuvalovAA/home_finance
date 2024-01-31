from django.core.management.base import BaseCommand
from user.models import User
from datetime import datetime

class Command(BaseCommand):
    """Команда кастомизированная для создания суперпользователя.
    
    Пример:
    poetry run python manage.py custom_createsuperuser <phone> <email> <password>
    """

    def add_arguments(self, parser):
        "Добавление аргументов из треминальной строки"
        parser.add_argument("phone", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)

    def handle(self, *args, **options):
        phone = options["phone"]
        email = options["email"]
        password = options["password"]
        user = User.objects.create_superuser(
            username=phone,
            phone=phone,
            email=email,
            birth_date=datetime.now(),
            register_date=datetime.now(),
            sms_subcribe=False,
            email_subcribe=False,
            is_active=True,
            is_service_account=True

        )
        user.set_password(password)
        user.save()

        print('OK')
