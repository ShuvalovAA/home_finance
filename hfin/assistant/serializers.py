from rest_framework import serializers

class GetPredictSerializer(serializers.Serializer):
    """Сериалайзер для предсказания расходы."""

    user_id = serializers.IntegerField()
    expense_name = serializers.CharField()
