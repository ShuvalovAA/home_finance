from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
from datetime import timedelta


class User(AbstractUser):
    """Модель пользователя."""

    first_name = models.CharField(max_length=124)
    last_name = models.CharField(max_length=124)
    middle_name = models.CharField(max_length=124)
    email = models.EmailField(max_length=254)
    birth_date = models.DateTimeField()
    register_date = models.DateField()
    sms_subcribe = models.BooleanField()
    email_subcribe = models.BooleanField()
    is_active = models.BooleanField()
    is_service_account = models.BooleanField()
    phone = PhoneNumberField(blank=True, null=False, unique=True)
    is_phone_confirm = models.BooleanField(blank=True, default=False)
    is_email_confirm = models.BooleanField(blank=True, default=False)

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class UserPhoneConfirmSMS(models.Model):
    """Модель смс подтверждения телефона."""

    NOW = now()
    number = models.IntegerField()
    user = models.ForeignKey(User, models.CASCADE)
    create_date = models.DateField(default=NOW)
    expare_date = models.DateField(default=NOW + timedelta(minutes=1))
