from income.models import Income
from expense.models import Expense
from transaction.models import Transaction
from django.db.models import Sum


class FundsDirector:
    """Директор построения фондов: доходов, расходов, транзакций пользователя."""

    def __init__(self, user_id: int):
        self.user_id = user_id

    def build_funds_income(self):
        "Построить фонды доходов."
        incomes_funds_qs = Income.objects.filter(
            user_id=self.user_id
        ).values('name', 'done').annotate(sum_amount=Sum('amount'))
        if not incomes_funds_qs:
            raise Income.DoesNotExist

        incomes_names = set(raw['name'] for raw in incomes_funds_qs)
        incomes_dict = {name: {'done': 0, 'not_done': 0} for name in incomes_names}

        for raw in incomes_funds_qs:
            if raw['done']:
                incomes_dict[raw['name']]['done'] = raw['sum_amount']
            else:
                incomes_dict[raw['name']]['not_done'] = raw['sum_amount']

        return incomes_dict

    def build_funds_expense(self):
        "Построить фонды расходов."
        expense_funds_qs = Expense.objects.filter(
            user_id=self.user_id
        ).values('name', 'done').annotate(sum_amount=Sum('amount'))
        if not expense_funds_qs:
            raise Expense.DoesNotExist

        expense_names = set(raw['name'] for raw in expense_funds_qs)
        expense_dict = {name: {'done': 0, 'not_done': 0} for name in expense_names}

        for raw in expense_funds_qs:
            if raw['done']:
                expense_dict[raw['name']]['done'] = raw['sum_amount']
            else:
                expense_dict[raw['name']]['not_done'] = raw['sum_amount']

        return expense_dict

    def build_funds_transaction(self):
        "Построить фонды транзакций."
        transaction_funds_qs = Transaction.objects.filter(
            user_id=self.user_id
        ).values('name').annotate(sum_amount=Sum('amount'))
        if not transaction__funds_qs:
            raise Transaction.DoesNotExist

        transaction_names = set(raw['name'] for raw in transaction_funds_qs)
        transaction_dict = {name: {'done': 0} for name in transaction_names}

        for raw in transaction_funds_qs:
            transaction_dict[raw['name']]['done'] = raw['sum_amount']

        return transaction_dict
