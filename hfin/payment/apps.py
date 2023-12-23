from django.apps import AppConfig


class PaymentConfig(AppConfig):
    """Конфиг подмели оплат пользователей."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
