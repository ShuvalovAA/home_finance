from django.db import models

from root.settings import AUTH_USER_MODEL


class Transaction(models.Model):
    """Модель транзакции."""

    name = models.fields.TextField(null=False)
    date = models.fields.DateTimeField(null=False)
    amount = models.fields.DecimalField(null=False, max_digits=21, decimal_places=2)
    user_id = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
