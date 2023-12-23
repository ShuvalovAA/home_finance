from django.apps import AppConfig


class UserConfig(AppConfig):
    """Конфиг модели пользователя."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
