from rest_framework import serializers
from .models import Tariff


class SendSerializer(serializers.Serializer):
    """Сериалайзер для отправки платежа."""

    tariff = serializers.ChoiceField(Tariff.CHOICES_PERIOD_MOTNHS)
    user_id = serializers.IntegerField()


class GetByUserSerializer(serializers.Serializer):
    """Сериалайзер для выборки данных по платежам у пользователя."""

    user_id = serializers.IntegerField()


class GetSerializer(serializers.Serializer):
    """Сериалайзер для получения платежа."""

    data = serializers.JSONField()
