from typing import Optional
from datetime import datetime
from income.models import Income
from expense.models import Expense
from transaction.models import Transaction
from django.db.models import Sum, Value, CharField


class Reporter:
    """Класс отчётов по доходам, расходам, транзакциям пользователя."""

    def __init__(self, user_id: int, start_period: Optional[datetime] = None, end_period: Optional[datetime] = None):
        self.user_id = user_id
        self.start_period = start_period
        self.end_period = end_period

    def get_years_list(self):
        """Получить список всех годов, которые есть в доходах или расходах."""
        Income.objects._using_default()
        incomes_years_list = list(Income.objects.filter(
            user_id=self.user_id
        ).values_list(
            'date__year', flat=True
            ).distinct()
        )
        Expense.objects._using_default()
        expense_years_list = list(Expense.objects.filter(
            user_id=self.user_id
        ).values_list(
            'date__year', flat=True
            ).distinct()
        )

        return set(incomes_years_list + expense_years_list)

    def get_income(self):
        "Получить словарь значений доходов."
        Income.objects._using_default()
        incomes_list = list(Income.objects.filter(
            user_id=self.user_id,
            date__gte=self.start_period,
            date__lte=self.end_period
        ).values_list(
            'date__date',
            ).annotate(
                amount=Sum('amount')
            ).values_list('date__date', 'amount')
        )
        return {'incomes': incomes_list}

    def get_expense(self):
        "Получить словарь значений расходов."
        Expense.objects._using_default()
        expense_list = list(Expense.objects.filter(
            user_id=self.user_id,
            date__gte=self.start_period,
            date__lte=self.end_period
        ).values_list(
            'date__date',
            ).annotate(
                amount=Sum('amount')
            ).values_list('date__date', 'amount')
        )
        return {'expenses': expense_list}

    def get_transaction(self):
        "Получить словарь значений транзакций."
        transaction_list = list(Transaction.objects.filter(
            user_id=self.user_id,
            date__gte=self.start_period,
            date__lte=self.end_period
        ).values_list(
            'date__date',
            ).annotate(
                amount=Sum('amount')
            ).values_list('date__date', 'amount')
        )
        return {'transactions': transaction_list}

    def get_grouping_income(self):
        """Получить сгрупиированные данные по доходам."""
        Income.objects._using_default()
        grouping_incomes = list(Income.objects.filter(
            user_id=self.user_id
        ).values_list(
            'name',
            ).annotate(
                amount=Sum('amount')
            ).values_list('name', 'amount')
        )

        return grouping_incomes

    def get_grouping_expense(self):
        """Получить сгрупиированные данные по расходам."""
        Expense.objects._using_default()
        grouping_incomes = list(Expense.objects.filter(
            user_id=self.user_id
        ).values_list(
            'name',
            ).annotate(
                amount=Sum('amount')
            ).values_list('name', 'amount')
        )

        return grouping_incomes

    def get_years_dataset(self):
        """Получит датасет за указанный год."""
        col_names = ['name', 'date', 'amount', 'type']
        Income.objects._using_default()
        incomes_years_list = list(
            Income.objects.filter(
                user_id=self.user_id,
                date__gte=self.start_period,
                date__lte=self.end_period
            ).annotate(
                type=Value('доход', output_field=CharField())
            ).values_list(
                'name', 'date__date', 'amount', 'type'
            )
        )

        Expense.objects._using_default()
        expense_years_list = list(
            Expense.objects.filter(
                user_id=self.user_id,
                date__gte=self.start_period,
                date__lte=self.end_period
            ).annotate(
                type=Value('расход', output_field=CharField())
            ).values_list(
                'name', 'date__date', 'amount', 'type'
            )
        )

        dataset = []
        dataset += [col_names]
        dataset += [list(i) for i in incomes_years_list]
        dataset += [list(i) for i in expense_years_list]

        return dataset
