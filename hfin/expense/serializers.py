from rest_framework import serializers

from .models import Expense


class CreateExpenseSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания модели расхода."""

    user_id = serializers.IntegerField()

    class Meta:
        """Метаданные сериалайзера."""

        model = Expense
        fields = [
            'name',
            'date',
            'amount',
            'done',
            'user_id'
        ]


class UpdateExpenseSerializer(serializers.ModelSerializer):
    """Сериалайзер для обновления модели расхода."""

    id = serializers.IntegerField(source='expense.id')
    user_id = serializers.IntegerField(source='expense.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Expense
        fields = [
            'id',
            'user_id',
            'name',
            'date',
            'amount',
            'done'
        ]


class UpdateExpenseBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового обновления модели расхода."""

    items = serializers.ListField(
        child=UpdateExpenseSerializer(),
        allow_empty=False,
        max_length=50
    )
    user_id = serializers.IntegerField()


class DeleteExpenseSerializer(serializers.ModelSerializer):
    """Сериалайзер для удаления модели расхода."""

    id = serializers.IntegerField(source='expense.id')
    user_id = serializers.IntegerField(source='expense.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Expense
        fields = ['id', 'user_id']


class DeleteExpenseBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового удаления модели расхода."""

    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        max_length=50
    )
    user_id = serializers.IntegerField()


class GetExpenseSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения модели расхода."""

    id = serializers.IntegerField(source='expense.id')
    user_id = serializers.IntegerField(source='expense.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Expense
        fields = ['id', 'user_id']


class NamesExpenseSerializer(serializers.Serializer):
    """Сериалайзер для получения списка наименования расходов."""

    user_id = serializers.IntegerField()

class GetExpenseBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового получения модели расхода."""

    page = serializers.IntegerField()
    user_id = serializers.IntegerField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    name = serializers.CharField(required=False)
    done = serializers.BooleanField(required=False)


class CountExpenseSerializer(serializers.Serializer):
    """Сериалайзер для получения количества элементов расходов."""

    user_id = serializers.IntegerField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    name = serializers.CharField(required=False)
    done = serializers.BooleanField(required=False)


class CopyExpenseSerializer(serializers.ModelSerializer):
    """Сериалайзер для копирования модели расхода."""

    id = serializers.IntegerField(source='expense.id')
    user_id = serializers.IntegerField(source='expense.user_id')

    class Meta:
        """Метаданные сериалайзера."""

        model = Expense
        fields = ['id', 'user_id']


class CopyExpenseBulkSerializer(serializers.Serializer):
    """Сериалайзер для массового копирования модели расхода."""

    items = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        max_length=50
    )
    user_id = serializers.IntegerField()


class CreateBulkExpenseSerializer(serializers.Serializer):
    """Сериалайзер для массового создания модели расхода."""

    file = serializers.FileField(max_length=100, allow_empty_file=False)
    user_id = serializers.IntegerField()
