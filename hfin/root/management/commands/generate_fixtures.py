from django.core.management.base import BaseCommand
from django.apps import apps
from root.settings import INSTALLED_APPS
from django_dynamic_fixture import G
from django_dynamic_fixture.ddf import BadDataError
from tqdm import tqdm


class Command(BaseCommand):
    """Команда генерации фикстур для пользовательских моделей.

    Пример использования:
    python manage.py generate_fixtures <количество фикстур, которые необходимо создать.>
    """
    help = "Команда генерирует тестовые данные для пользовательских моделей."
    INGNORE_APPS = [
        'userphoneconfirmsms',
        'user_user_permissions',
        'captchastore',
        'user_groups'
    ]

    def add_arguments(self, parser):
        "Добавление аргументов из треминальной строки"
        parser.add_argument("count_fixtures", type=int)

    def handle(self, *args, **options):
        count_fixtures = options["count_fixtures"]
        error_fixtures_dict = {}
        error_fixtures_count = 0
        for application_name in INSTALLED_APPS:
            application = apps.all_models[application_name]
            if application:
                error_fixtures_count = 0
                for model_name, model_class in application.items():
                    if model_name in self.INGNORE_APPS:
                        continue
                    for _ in tqdm(range(count_fixtures), desc=model_name):
                        try:
                            model_obj = G(model_class)
                        except BadDataError:
                            error_fixtures_count += 1
                            continue
                        model_obj.save()
                    error_fixtures_dict[application_name] = {"count": error_fixtures_count, 'model_class': model_class}

        if error_fixtures_dict:
            for model_name, model_info in error_fixtures_dict.items():
                for _ in tqdm(range(model_info['count']), desc=model_name):
                    model_obj = G(model_info['model_class'])
                    model_obj.save()
