from django.contrib.auth.models import AbstractUser
from django.db import models


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
    USERNAME_FIELD = 'username'
