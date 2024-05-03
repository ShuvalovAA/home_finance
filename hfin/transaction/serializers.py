from rest_framework import serializers

from .models import Transaction


class CountTransactionSerializer(serializers.Serializer):
    """Сериалайзер для получения количества элементов транзакции."""

    user_id = serializers.IntegerField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    name = serializers.CharField(required=False)


class CreateTransactionSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания модели транзакции."""

    user_id = serializers.IntegerField()

    class Meta:
        """Метаданные сериалайзера."""

        model = Transaction
        fields = [
            'name',
            'target_name',
            'date',
            'amount',
            'user_id'
        ]


class UpdateTransactionSerializer(serializers.ModelSerializer):
    """Сериалайзер для обновления модели транзакции."""

    id = serializers.IntegerField(source='transaction.id')
    user_id = serializers.IntegerField(source='transaction.user_id')

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
    user_id = serializers.IntegerField()


class DeleteTransactionSerializer(serializers.ModelSerializer):
    """Сериалайзер для удаления модели транзакции."""

    id = serializers.IntegerField(source='transaction.id')
    user_id = serializers.IntegerField(source='transaction.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Transaction
        fields = ['id', 'user_id']


class DeleteTransactionBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового удаления модели транзакции."""

    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        max_length=50
    )
    user_id = serializers.IntegerField()


class GetTransactionSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения модели транзакции."""

    id = serializers.IntegerField(source='transaction.id')
    user_id = serializers.IntegerField(source='transaction.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Transaction
        fields = ['id', 'user_id']


class GetTransactionBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового получения модели транзакции."""

    page = serializers.IntegerField()
    user_id = serializers.IntegerField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    names = serializers.JSONField(required=False)
    target_names = serializers.CharField(required=False)
    done = serializers.BooleanField(required=False)


class CopyTransactionSerializer(serializers.ModelSerializer):
    """Сериалайзер для копирования модели транзакции."""

    id = serializers.IntegerField(source='transaction.id')
    user_id = serializers.IntegerField(source='transaction.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Transaction
        fields = ['id', 'user_id']


class CopyTransactionBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового копирования модели транзакции."""

    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        max_length=50
    )
    user_id = serializers.IntegerField()


class DownloadFileSerializer(serializers.Serializer):
    """Сериалайзер для скачивания файла."""

    user_id = serializers.IntegerField()
    file_type = serializers.CharField()
    separator = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class TransactionDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['name', 'user_id']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        

        return data
