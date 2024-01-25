"""
https://translated.turbopages.org/proxy_u/en-ru.ru.7055a0a8-65afae38-7e82c3e0-74722d776562/https/www.geeksforgeeks.org/save-and-load-machine-learning-models-in-python-with-scikit-learn/
"""

import numpy as np
import datetime
from scipy import stats
from sklearn.linear_model import LinearRegression
from django.db.models import Sum
from decimal import Decimal
from expense.models import Expense
from root.settings import BASE_DIR
import joblib
import os


class MLLinearRegressionAmountExpense:
    """Класс для построения линейной регрессии в рамках определения будущих расходов."""
    MODELS_DIR = os.path.join(BASE_DIR, 'ml_models')

    def __init__(self):
        self.expense_model = Expense
        self.linear_model = LinearRegression()
        self.work_model = None
        self.months_of_year = None
        self.amounts = None

    def _build_model(self, user, expense_name):
        """Построить модель"""
        exists_model = self._get_model(models_name=expense_name)

        if exists_model:
            self.work_model = exists_model
            return

        expenses = list(
                Expense.objects.filter(
                done=True, # True
                name__iexact=expense_name,
                amount__gte=0
            ).values_list(
                'date__year',
                'date__month'
            ).annotate(
                total_amount=Sum('amount')
            ).values_list('date__year', 'date__month', 'total_amount')
        )

        if not expenses:
            raise Expense.DoesNotExist('Expense.DoesNotExist')

        self.months_of_year = np.array([(row[0]*100) + row[1] for row in expenses]).reshape((-1, 1))
        self.amounts = np.array([row[2] for row in expenses])

        self.work_model = self.linear_model.fit(self.months_of_year, self.amounts)
        #self._save_model(models_name=expense_name)

    def _save_model(self, models_name):
        """Сохранить модель."""
        # self.work_model
        pass

    def _get_model(self, models_name):
        """Получить готовую модель."""
        pass

    def get_prediction(self, user, expense_name):
        """Получить предсказание расхода на день года."""
        self._build_model(
            user,
            expense_name
        )
        determination = self.work_model.score(self.months_of_year, self.amounts)

        if determination < 0.5:
            print(f'bad determination: {determination} \n coef: {self.work_model.coef_}')
        else:
            print(f'good determination: {determination} \n coef: {self.work_model.coef_}')

        year = datetime.datetime.now().year
        months = []
        for m in range(1, 13, 1):
            months.append((year * 100) + m)
        months = np.array(months).reshape((-1, 1))
        predict_result = self.work_model.predict(months)
        days = [i[0] for i in months]
        amounts = [round(Decimal(i), 2) for i in predict_result]
        data = []

        mode_result = stats.mode([float(i) for i in self.amounts])
        deviations = []
        for i in amounts:
            deviations.append(float(mode_result.mode) / float(i) )
        deviation_mode = stats.mode(deviations).mode

        for i in range(0, len(days), 1):
            amount = amounts[i]
            if self.work_model.coef_[0] > 50:
                amount = round(Decimal(float(amount) / self.work_model.coef_[0] * 100), 2)
            data.append(
                {
                    "year": int(days[i] / 100),
                    "month": days[i] % 100,
                    "amount": amount
                }
            )
        mode_result = stats.mode([float(i) for i in self.amounts])
        median = np.median(self.amounts)
        return data, Decimal(mode_result.mode), median


ml_linear_regression = MLLinearRegressionAmountExpense()
