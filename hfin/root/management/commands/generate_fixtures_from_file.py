from django.core.management.base import BaseCommand
import pandas
from expense.models import Expense
from income.models import Income
from user.models import User
from tqdm import tqdm
from datetime import datetime
from decimal import Decimal


class Command(BaseCommand):
    """Команда генерации фикстур для пользовательской модели расходов.

    Пример использования:
    python manage.py generate_fixtures_from_file <путь до файла> <id пользователя> <expense|income>
    Подерживается файл формата .xlsx
    """
    help = "Команда генерирует тестовые данные для пользовательской модели расходов."

    def add_arguments(self, parser):
        "Добавление аргументов из треминальной строки"
        parser.add_argument("file_path", type=str)
        parser.add_argument("user_id", type=int)
        parser.add_argument("type", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        user_id = options["user_id"]
        type_operatoin = options['type']

        if type_operatoin == 'expense':
            user = User.objects.get(pk=user_id)
            data = pandas.read_excel(file_path)
            expenses_objs = []
            for i in tqdm(range(len(data))):
                params = {
                    'name': data['name'][i].lower(),
                    'date': datetime.strptime(str(data['date'][i]), '%Y-%m-%d %H:%M:%S').date(),
                    'amount': data['amount'][i] if data['amount'][i] >= 0 else 0,
                    'done': True if data['done'][i] == 'Исполнено' else False,
                    'user': user
                }
                expense_obj = Expense(**params)
                expenses_objs.append(expense_obj)

            Expense.objects.bulk_create(expenses_objs)

        if type_operatoin == 'income':
            user = User.objects.get(pk=user_id)
            data = pandas.read_excel(file_path)
            incomes_objs = []
            for i in tqdm(range(len(data))):
                params = {
                    'name': data['name'][i].lower(),
                    'date': datetime.strptime(str(data['date'][i]), '%d.%m.%Y').date(),
                    'amount': Decimal(data['amount'][i]) if Decimal(data['amount'][i]) >= 0 else 0,
                    'done': True if data['done'][i] == 'Исполнено' else False,
                    'user': user
                }
                income_obj = Income(**params)
                incomes_objs.append(income_obj)

            Income.objects.bulk_create(incomes_objs)
