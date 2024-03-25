from django.db import models
from root.settings import AUTH_USER_MODEL
from root.managers import RoutedManager
from django.core.validators import MaxValueValidator, MinValueValidator

class Transaction(models.Model):
    """Модель транзакции."""

    name = models.fields.TextField(null=False)
    target_name = models.fields.TextField(null=False)
    date = models.fields.DateTimeField(null=False)
    amount = models.fields.DecimalField(null=False, max_digits=21, decimal_places=2, validators=[MinValueValidator(0)])
    user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE)

    objects = RoutedManager()
