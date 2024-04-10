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


class GetExpense(GetBase):
    """Сериалайзер для получения всех расходов пользователя."""


class GetTransaction(GetBase):
    """Сериалайзер для получения всех  транзакций пользователя."""
