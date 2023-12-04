"""Ошибки серсива мигратера логов DML."""
__all__ = [
    'ServiceError',
    'DataNotFound'
]

class ServiceError(Exception):
    """Базовая ошибка вызова сервиса."""

class DataNotFound(ServiceError):
    """Данные не найдены."""

    message = "Данные за указанный период не найдены."


class ThrottlingError(ServiceError):
    """Нарушены условия тротлинга"""

    message = "Выгрузка данных находится в процессе выполнения или с последней выгрузки не прошло 15 минут."

