from typing import Optional
from datetime import datetime
from income.models import Income
from expense.models import Expense
from transaction.models import Transaction


class Reporter:
    """Класс отчётов по доходам, расходам, транзакциям пользователя."""

    def __init__(self, user_id: int, start_period: Optional[datetime] = None, end_period: Optional[datetime] = None):
        self.user_id = user_id
        self.start_period = start_period
        self.end_period = end_period

    def get_income(self):
        "Получить словарь значений доходов."
        incomes_list = list(Income.objects.filter(
            user_id=self.user_id,
            date__gte=self.start_period,
            date__lte=self.end_period
        ).only('name', 'date', 'amount', 'done').values())
        return {'incomes': incomes_list}

    def get_expense(self):
        "Получить словарь значений расходов."
        expense_list = list(Expense.objects.filter(
            user_id=self.user_id,
            date__gte=self.start_period,
            date__lte=self.end_period
        ).only('name', 'date', 'amount', 'done').values())
        return {'expenses': expense_list}

    def get_transaction(self):
        "Получить словарь значений транзакций."
        transaction_list = list(Transaction.objects.filter(
            user_id=self.user_id,
            date__gte=self.start_period,
            date__lte=self.end_period
        ).only('name', 'date', 'amount').values())
        return {'transactions': transaction_list}
