from root.settings import NEED_TABLE_ROUTING


class DBRouter:
    """Маршрутизатор запросов к базам данных."""
    def __init__(self):
        pass

    def db_for_read(self, model, **hints):
        """Маршрут на чтение данных."""
        if model._meta.db_table in NEED_TABLE_ROUTING:
            return "clickhouse"

        return 'default'

    def db_for_write(self, model, **hints):
        """Маршрут на запись данных."""
        return "default"

    def db_for_delete(self, model, **hints):
        """Маршрут на удаления данных."""
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Разрещение на миграцию."""
        return True
