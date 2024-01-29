from .models import Notification

class Notificator:
    """Класс нотификатора для взаимодействия с уведомлениями пользователей."""

    def __init__(self, user) -> None:
        self.user = user

    def get_notifications(self):
        """Получить уведомления."""
        notifications = Notification.objects.filter(user=self.user)
        return notifications

    def set_notification(self, event_type, event_date, detail_info):
        """Установить уведомление."""

        notification = Notification(
            event_date=event_date,
            detail_info=detail_info,
            event_type=event_type
        )
        notification.save()
