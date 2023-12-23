from django.db import models

# from user.models import User


class Expense(models.Model):
    """Модель расхода."""

    name = models.fields.TextField(null=False)
    date = models.fields.DateTimeField(null=False)
    amount = models.fields.DecimalField(null=False, max_digits=21, decimal_places=2)
    done = models.fields.BooleanField(null=False)
    # user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
