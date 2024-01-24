"""
https://translated.turbopages.org/proxy_u/en-ru.ru.7055a0a8-65afae38-7e82c3e0-74722d776562/https/www.geeksforgeeks.org/save-and-load-machine-learning-models-in-python-with-scikit-learn/
"""

import numpy as np
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
        self.days_of_year = None
        self.amounts = None

    def _build_model(self, user, expense_name):
        """Построить модель"""
        exists_model = self._get_model(models_name=expense_name)

        if exists_model:
            self.work_model = exists_model
            return

        # expenses = list(Expense.objects.filter(
        #     done=True, # True
        #     name__iexact=expense_name
        # ).annotate(total_amount=Sum('amount')).values('date').values_list('date', 'amount'))
        expenses = list(Expense.objects.filter(
            done=True, # True
            name__iexact=expense_name
        ).values_list('date').annotate(total_amount=Sum('amount')))

        if not expenses:
            raise Expense.DoesNotExist('Expense.DoesNotExist')

        self.days_of_year = np.array([row[0].timetuple().tm_yday for row in expenses]).reshape((-1, 1))
        self.amounts = np.array([row[1] for row in expenses])

        self.work_model = self.linear_model.fit(self.days_of_year, self.amounts)
        self._save_model(models_name=expense_name)

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
        determination = self.work_model.score(self.days_of_year, self.amounts)

        if determination < 0.5:
            print('bad determination')
        else:
            print('good determination')

        predict_days_of_years = np.array([ z for z in set([i[0] for i in self.days_of_year])]).reshape((-1, 1))
        predict_result = self.work_model.predict(predict_days_of_years)
        
        days = [i[0] for i in predict_days_of_years]
        amounts = [round(Decimal(i), 2) for i in predict_result]
        data = []
        for i in range(0, len(days)-1, 1):
            data.append(
                {
                    "day_of_year": days[i],
                    "month_of_year": int(days[i] / 30)+1,
                    "amount": amounts[i]
                }
            )

        return data


ml_linear_regression = MLLinearRegressionAmountExpense()
