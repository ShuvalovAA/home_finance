from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):
#     """Модель пользователя."""

#     first_name = models.TextField()
#     last_name = models.TextField()
#     middle_name = models.TextField()
#     phone = models.PhoneNumberField((""))
#     email = models.EmailField((""), max_length=254)
#     birth_date = models.DateTimeField()
#     register_date = models.DateField()
#     sms_subcribe = models.BooleanField()
#     email_subcribe = models.BooleanField()
#     is_active = models.BooleanField()
#     is_service_account = models.BooleanField()
#     password = models.TextField()
