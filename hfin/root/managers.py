import copy

from django.db.models import Manager
from root.settings import DATABASES
from django.db.models import QuerySet
from django.db.models.deletion import Collector


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

    def delete(self):
        """Delete the records in the current QuerySet."""
        self._not_support_combined_queries("delete")
        if self.query.is_sliced:
            raise TypeError("Cannot use 'limit' or 'offset' with delete().")
        if self.query.distinct_fields:
            raise TypeError("Cannot call delete() after .distinct(*fields).")
        if self._fields is not None:
            raise TypeError("Cannot call delete() after .values() or .values_list()")

        del_query = self._chain()

        # The delete is actually 2 queries - one to find related objects,
        # and one to delete. Make sure that the discovery of related
        # objects is performed on the same database as the deletion.
        del_query._for_write = True

        # Disable non-supported fields.
        del_query.query.select_for_update = False
        del_query.query.select_related = False
        del_query.query.clear_ordering(force=True)

        collector = Collector(using='default', origin=self)
        collector.collect(del_query)
        deleted, _rows_count = collector.delete()

        # Clear the result cache, in case this QuerySet gets reused.
        self._result_cache = None
        return deleted, _rows_count


class RoutedManager(Manager):
    """Маршрутизированный менеджер взаимодействия с базами данных."""

    def get_queryset(self):
        return RotedQuerySet(model=self.model, using=self._db, hints=self._hints)
