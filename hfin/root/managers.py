import copy

from django.db.models import Manager
from root.settings import DATABASES
from django.db.models import QuerySet


def _get_db_queue():
    """Получить сортированную очередь имён баз данных для последовательного запроса."""
    db_names = [name for name in DATABASES.keys()]
    db_queue = copy.deepcopy(db_names)
    for db_name in db_names:
        index = len(db_names) - DATABASES[db_name]['priority']
        db_queue[index] = db_name
    return db_queue


class RotedQuerySet(QuerySet):
    """Кастомизированый построитель запросов для маршрутизации."""

    def _filter(self, *args, **kwargs):
        """
        Return a new QuerySet instance with the args ANDed to the existing
        set.
        """
        self._not_support_combined_queries("filter")
        return self._filter_or_exclude(False, args, kwargs)

    def filter(self, *args, **kwargs):
        db_queue = _get_db_queue()
        for db in db_queue:
            print(db)
            result = self._filter(*args, **kwargs).using(db)
            #а если ответ не пустой, но там нет нового значения?
            if result:
                return result
        return result


class RoutedManager(Manager):
    """Маршрутизированный менеджер взаимодействия с базами данных."""

    def get_queryset(self):
        return RotedQuerySet(model=self.model, using=self._db, hints=self._hints)
