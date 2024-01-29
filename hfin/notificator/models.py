from django.db import models
from root.settings import AUTH_USER_MODEL


class Notification(models.Model):
    """Модель уведомления."""
    EVENTS_TYPES = (
        (1, 'getting_income'), 
        (2, 'subscribe_expiring'),
        (3, 'expense outside income')
    )
    user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE)
    event_date = models.fields.DateTimeField(null=False)
    event_type = models.CharField(choices=EVENTS_TYPES, max_length=1)
    detail_info = models.JSONField(encoder='utf-8', decoder='utf-8')
