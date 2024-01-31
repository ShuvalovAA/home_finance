from datetime import timedelta

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField


class CustomtUserManager(BaseUserManager):
    """Кастомизированный менеджер управления моделью пользователя."""

    def create_superuser(self, phone, password=None, **extra_fields):
        """Создать суперпользователя."""
        password = password if password else 'test'
        user = User.objects.create(phone, extra_fields.get('email'), "test")
        user.set_password(password)
        user.is_superuser = True
        user.is_service_account = True
        user.save(using=self._db)


class User(AbstractUser):
    """Модель пользователя."""

    first_name = models.CharField(max_length=124)
    last_name = models.CharField(max_length=124)
    middle_name = models.CharField(max_length=124)
    email = models.EmailField(max_length=254)
    birth_date = models.DateTimeField(null=True)
    register_date = models.DateField()
    sms_subcribe = models.BooleanField()
    email_subcribe = models.BooleanField()
    is_active = models.BooleanField()
    is_service_account = models.BooleanField()
    phone = PhoneNumberField(blank=True, null=False, unique=True)
    is_phone_confirm = models.BooleanField(blank=True, default=False)
    is_email_confirm = models.BooleanField(blank=True, default=False)
    email_token = models.CharField(max_length=100, null=True)
    enable_subscription = models.BooleanField(blank=True, default=False)

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def activate_subscription(self):
        self.enable_subscription = True
        self.save()

    def deactivate_subscription(self):
        self.enable_subscription = False
        self.save()


class UserPhoneConfirmSMS(models.Model):
    """Модель смс подтверждения телефона."""

    NOW = now()
    number = models.IntegerField()
    user = models.ForeignKey(User, models.CASCADE)
    create_date = models.DateTimeField(default=NOW)
    expare_date = models.DateTimeField(default=NOW + timedelta(minutes=1))
