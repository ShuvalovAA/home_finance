import requests
import datetime
import itertools
import json
from typing import Optional
from datetime import datetime
from user.models import User
from income.models import Income
from expense.models import Expense
from transaction.models import Transaction
from django.db.models import Sum, Value, CharField
from assistant.handlers import ml_linear_regression
from root.settings import INFLATION_LOCATION, INFLATION_API_KEY


def get_inflation():
    """Получить процент инфляции"""
    country = INFLATION_LOCATION
    api_url = 'https://api.api-ninjas.com/v1/inflation?country={}'.format(country)
    response = requests.get(api_url, headers={'X-Api-Key': INFLATION_API_KEY})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

    return json.loads(response.text)[0]


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
        col_names = ['name', 'year', 'month', 'day', 'amount', 'type']
        Income.objects._using_default()
        incomes_years_list = list(
            Income.objects.filter(
                user_id=self.user_id,
            ).annotate(
                type=Value('доход', output_field=CharField())
            ).values_list(
                'name', 'date__year', 'date__month', 'date__day', 'amount', 'type'
            )
        )

        Expense.objects._using_default()
        expense_years_list = list(
            Expense.objects.filter(
                user_id=self.user_id
            ).annotate(
                type=Value('расход', output_field=CharField())
            ).values_list(
                'name', 'date__year', 'date__month', 'date__day', 'amount', 'type'
            )
        )

        dataset = []
        dataset += [col_names]
        dataset += [list(i) for i in incomes_years_list]
        dataset += [list(i) for i in expense_years_list]

        return dataset

    def get_years_dataset_transaction(self):
        """Получит датасет по транзакциям."""
        col_names = ['name', 'target_name', 'year', 'month', 'day', 'amount']
        Transaction.objects._using_default()
        transaction_years_list = list(
            Transaction.objects.filter(
                user_id=self.user_id,
            ).annotate(
                type=Value('доход', output_field=CharField())
            ).values_list(
                'name', 'target_name', 'date__year', 'date__month', 'date__day', 'amount'
            )
        )

        dataset = []
        dataset += [col_names]
        dataset += [list(i) for i in transaction_years_list]

        return dataset

    def get_predict_day_of_year(self):
        """Вернуть предсказение расходов с учётом инфляции на два года вперёд."""
        user = User.objects.get(pk=self.user_id)
        now_year = datetime.now().year
        years = [now_year + year for year in range(1, 3, 1)]
        inflation_prct = get_inflation()
        col_names = ['year', 'month', 'amount', 'name']

        dataset = []
        dataset += [col_names]
        expense_names_list = list(
            Expense.objects.filter(
                user_id=self.user_id
            ).values_list(
                'name', flat=True
            )
        )
        #подумать куда вставить инфляцию
        expense_names_list = [expense_n for expense_n in set(expense_names_list)]
        for year, expense_name in itertools.product(years, expense_names_list):
            data_expense_predict = ml_linear_regression.get_prediction(
                user, expense_name.lower(), year
            )
            print(year, expense_name, data_expense_predict[0])
            if len(data_expense_predict[0]) == 0:
                continue
            rows = [[row['year'], row['month'], row['amount']] for row in data_expense_predict[0]]
            [row.append(expense_name) for row in rows]

            dataset += rows

        return dataset
