import random
import os
import struct

from django.utils.timezone import now

from .models import User, UserPhoneConfirmSMS


def create_sms_confirm(user: User):
    """Создать смс подтверждения телефона объекта в базе данных."""
    code_in_bd = UserPhoneConfirmSMS.objects.filter(user=user, expare_date__gte=now())
    if code_in_bd:
        return
    first_number = struct.unpack('H', os.urandom(2))[0]
    suff = str(struct.unpack('H', os.urandom(2))[0])[2]
    number = f'{first_number}{suff}'
    number = int(number)
    print(f'CODE:\t {number}')
    UserPhoneConfirmSMS.objects.create(number=number, user=user)


def create_email_confirm(user: User):
    """Создать подтверждение email и отправить."""
    LEN_NUMBER = 100
    MAX_NUMBER = 999999
    token = random.randrange(0, MAX_NUMBER, LEN_NUMBER)
    user.email_token = str(token)
    user.save()
    # message = f'Hi paste your link to verify your account http://localhost:80/verify/{token}'
    # recipient_list = [user.email]
    # send_mail(subject, message , email_from ,recipient_list)


def confirm_login(user: User, code: int):
    """Подвердить номер телефона."""
    code_in_bd = UserPhoneConfirmSMS.objects.filter(number=code, user=user, expare_date__gte=now())
    if not code_in_bd:
        # CodeExpireError
        raise ValueError


def confirm_phone(user: User, code: int):
    """Подвердить номер телефона."""
    code_in_bd = UserPhoneConfirmSMS.objects.filter(number=code, user=user, expare_date__gte=now()).last()
    if not code_in_bd:
        # CodeExpireError
        raise ValueError
    user.is_active = True
    user.is_phone_confirm = True
    user.save()
