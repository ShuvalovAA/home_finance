from django.db import models


class Tariff(models.Model):
    """Модель тарифа."""

    CHOICES_PERIOD_MOTNHS = [1, 2, 3]

    name = models.TextField()
    price = models.DecimalField()
    period_months = models.CharField(choices=CHOICES_PERIOD_MOTNHS)
