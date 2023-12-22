from django.db import models


class Income(models.Model):
    """Модель дохода."""

    name = models.fields.TextField(null=False)
    date = models.fields.DateTimeField(null=False)
    amount = models.fields.DecimalField(null=False, max_digits=21, decimal_places=2)
