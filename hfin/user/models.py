from django.db import models
from root.models import Tariff


class User(models.Model):
    """Модель пользователя."""

    first_name = models.TextField()
    last_name = models.TextField()
    middle_name = models.TextField()
    phone = models.PhoneNumberField((""))
    email = models.EmailField((""), max_length=254)
    birth_date = models.DateTimeField()
    register_date = models.DateField()
    sms_subcribe = models.BooleanField()
    email_subcribe = models.BooleanField()
    is_active = models.BooleanField()


class UsersPayments(models.Model):
    """Платежи пользователей."""

    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField()
    tariff = models.ForeignKey(to=Tariff, on_delete=models.CASCADE, null=False)
    done = models.BooleanField()
