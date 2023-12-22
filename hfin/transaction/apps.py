from django.apps import AppConfig


class TransactionConfig(AppConfig):
    """Конфигурация модели transaction."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transaction'
