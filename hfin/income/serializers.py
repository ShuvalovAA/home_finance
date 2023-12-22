from rest_framework import serializers

from .models import Income


class CreateIncomeSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания модели дохода."""

    class Meta:
        """Метаданные сериалайзера."""

        model = Income
        fields = '__all__'


class UpdateIncomeSerializer(serializers.ModelSerializer):
    """Сериалайзер для обновления модели дохода."""

    id = serializers.IntegerField(source='income.id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Income
        fields = '__all__'


class UpdateIncomeBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового обновления модели дохода."""

    items = serializers.ListField(
        child=UpdateIncomeSerializer(),
        allow_empty=False,
        max_length=50
    )


class DeleteIncomeSerializer(serializers.ModelSerializer):
    """Сериалайзер для удаления модели дохода."""

    id = serializers.IntegerField(source='income.id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Income
        fields = ['id']


class DeleteIncomeBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового удаления модели дохода."""

    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        max_length=50
    )


class GetIncomeSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения модели дохода."""

    id = serializers.IntegerField(source='income.id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Income
        fields = ['id']


class GetIncomeBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового получения модели дохода."""

    page = serializers.IntegerField()


class CopyIncomeSerializer(serializers.ModelSerializer):
    """Сериалайзер для копирования модели дохода."""

    id = serializers.IntegerField(source='income.id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Income
        fields = ['id']


class CopyIncomeBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового копирования модели дохода."""

    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        max_length=50
    )


class CreateBulkIncomeSerializer(serializers.Serializer):
    """Сериалайзер для массового создания модели дохода."""

    file = serializers.FileField(max_length=100, allow_empty_file=False)
