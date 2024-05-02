from rest_framework import serializers


class GetBase(serializers.Serializer):
    """Общий сериалайзер."""

    user_id = serializers.IntegerField()
    start_period = serializers.DateField()
    end_period = serializers.DateField()


class GetIncome(GetBase):
    """Сериалайзер для получения всех доходов пользователя."""


class GetIncomeGroup(serializers.Serializer):
    """Сериалайзер для получения всех доходов пользователя сгруппированными."""

    user_id = serializers.IntegerField()


class GetExpenseGroup(serializers.Serializer):
    """Сериалайзер для получения всех расходов пользователя сгруппированными."""

    user_id = serializers.IntegerField()


class GetYearsList(serializers.Serializer):
    """Сериалайзер для получения списка всех годов, которые есть в доходах или расходах."""

    user_id = serializers.IntegerField()


class GetYearsDatasetTransaction(serializers.Serializer):
    """Сериалайзер для получения получения датасета по транзакциям."""

    user_id = serializers.IntegerField()


class GetYearsPredictExpense(serializers.Serializer):
    """Сериалайзер для получения предсказаний на два года."""

    user_id = serializers.IntegerField()


class GetYearsDataset(serializers.Serializer):
    """Сериалайзер для получения получения датасета по доходам и расходам."""

    user_id = serializers.IntegerField()


class GetExpense(GetBase):
    """Сериалайзер для получения всех расходов пользователя."""


class GetTransaction(GetBase):
    """Сериалайзер для получения всех  транзакций пользователя."""
