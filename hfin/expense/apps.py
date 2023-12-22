from django.apps import AppConfig


class ExpenseConfig(AppConfig):
    """Конфигурация модели expense."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expense'
