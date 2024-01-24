from rest_framework import serializers


class FundsBuilderBase(serializers.Serializer):
    """Общий сериалайзер."""

    user_id = serializers.IntegerField()


class FundsBuilderIncome(FundsBuilderBase):
    """Сериалайзер для получения всех доходов пользователя."""


class FundsBuilderExpense(FundsBuilderBase):
    """Сериалайзер для получения всех расходов пользователя."""


class FundsBuilderTransaction(FundsBuilderBase):
    """Сериалайзер для получения всех  транзакций пользователя."""