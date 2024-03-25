from django.db import models
from root.settings import AUTH_USER_MODEL
from root.managers import RoutedManager
from django.core.validators import  MinValueValidator

class Income(models.Model):
    """Модель дохода."""

    name = models.fields.TextField(null=False)
    date = models.fields.DateTimeField(null=False)
    amount = models.fields.DecimalField(null=False, max_digits=21, decimal_places=2, validators=[MinValueValidator(0)])
    done = models.fields.BooleanField(null=False, blank=False)
    user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE)
    
    objects = RoutedManager()
