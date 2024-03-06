from rest_framework import serializers

from .models import Income


class CreateIncomeSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания модели дохода."""

    user_id = serializers.IntegerField()

    class Meta:
        """Метаданные сериалайзера."""

        model = Income
        fields = [
            'name',
            'date',
            'amount',
            'done',
            'user_id'
        ]


class UpdateIncomeSerializer(serializers.ModelSerializer):
    """Сериалайзер для обновления модели дохода."""

    id = serializers.IntegerField(source='income.id')
    user_id = serializers.IntegerField(source='income.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Income
        fields = [
            'id',
            'user_id',
            'name',
            'date',
            'amount',
            'done'
        ]


class UpdateIncomeBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового обновления модели дохода."""

    items = serializers.ListField(
        child=UpdateIncomeSerializer(),
        allow_empty=False,
        max_length=50
    )
    user_id = serializers.IntegerField()


class DeleteIncomeSerializer(serializers.ModelSerializer):
    """Сериалайзер для удаления модели дохода."""

    id = serializers.IntegerField(source='income.id')
    user_id = serializers.IntegerField(source='income.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Income
        fields = ['id', 'user_id']


class DeleteIncomeBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового удаления модели дохода."""

    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        max_length=50
    )
    user_id = serializers.IntegerField()


class GetIncomeSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения модели дохода."""

    id = serializers.IntegerField(source='income.id')
    user_id = serializers.IntegerField(source='income.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Income
        fields = ['id', 'user_id']


class NamesIncomeSerializer(serializers.Serializer):
    """Сериалайзер для получения списка наименования доходов."""

    user_id = serializers.IntegerField()

class GetIncomeBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового получения модели дохода."""

    page = serializers.IntegerField()
    user_id = serializers.IntegerField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    name = serializers.CharField(required=False)
    done = serializers.BooleanField(required=False)


class CountIncomeSerializer(serializers.Serializer):
    """Сериалайзер для получения количества элементов доходов."""

    user_id = serializers.IntegerField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    name = serializers.CharField(required=False)
    done = serializers.BooleanField(required=False)


class CopyIncomeSerializer(serializers.ModelSerializer):
    """Сериалайзер для копирования модели дохода."""

    id = serializers.IntegerField(source='income.id')
    user_id = serializers.IntegerField(source='income.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Income
        fields = ['id', 'user_id']


class CopyIncomeBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового копирования модели дохода."""

    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        max_length=50
    )
    user_id = serializers.IntegerField()


class CreateBulkIncomeSerializer(serializers.Serializer):
    """Сериалайзер для массового создания модели дохода."""

    file = serializers.FileField(max_length=100, allow_empty_file=False)
    user_id = serializers.IntegerField()
