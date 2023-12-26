from django.db import models
from root.settings import AUTH_USER_MODEL

class Tariff(models.Model):
    """Модель тарифа."""

    CHOICES_PERIOD_MOTNHS = ((1, ' One'), (2, 'Two'), (3, 'Three'))

    name = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=21)
    period_months = models.CharField(choices=CHOICES_PERIOD_MOTNHS, max_length=1)


class UsersPayments(models.Model):
    """Платежи пользователей."""

    user_id = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    tariff = models.ForeignKey(to=Tariff, on_delete=models.CASCADE, null=False)
    done = models.BooleanField()
