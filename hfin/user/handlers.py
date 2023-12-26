from .models import UserPhoneConfirmSMS, User
import random

def create_sms_confirm(user: User):
    """Создать смс подтверждения телефона объекта в базе данных."""
    LEN_NUMBER = 6
    MAX_NUMBER = 999999
    number = random.randrange(0, MAX_NUMBER, LEN_NUMBER)
    UserPhoneConfirmSMS.objects.create(number=number, user=user)


def confirm_phone():
    pass

def confirm_email():
    pass