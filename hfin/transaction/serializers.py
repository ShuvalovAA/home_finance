from rest_framework import serializers

from .models import Transaction


class CreateTransactionSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания модели транзакции."""

    class Meta:
        """Метаданные сериалайзера."""

        model = Transaction
        fields = '__all__'


class UpdateTransactionSerializer(serializers.ModelSerializer):
    """Сериалайзер для обновления модели транзакции."""

    id = serializers.IntegerField(source='transaction.id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Transaction
        fields = '__all__'


class UpdateTransactionBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового обновления модели транзакции."""

    items = serializers.ListField(
        child=UpdateTransactionSerializer(),
        allow_empty=False,
        max_length=50
    )


class DeleteTransactionSerializer(serializers.ModelSerializer):
    """Сериалайзер для удаления модели транзакции."""

    id = serializers.IntegerField(source='transaction.id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Transaction
        fields = ['id']


class DeleteTransactionBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового удаления модели транзакции."""

    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        max_length=50
    )


class GetTransactionSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения модели транзакции."""

    id = serializers.IntegerField(source='transaction.id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Transaction
        fields = ['id']


class GetTransactionBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового получения модели транзакции."""

    page = serializers.IntegerField()


class CopyTransactionSerializer(serializers.ModelSerializer):
    """Сериалайзер для копирования модели транзакции."""

    id = serializers.IntegerField(source='transaction.id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Transaction
        fields = ['id']


class CopyTransactionBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового копирования модели транзакции."""

    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        max_length=50
    )
