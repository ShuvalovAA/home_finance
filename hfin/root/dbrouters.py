from root.settings import NOT_TECH_MODELS, TECH_TABLES


class DBRouter:
    """Маршрутизатор запросов к базам данных."""
    def __init__(self):
        pass

    def db_for_read(self, model, **hints):
        """Маршрут на чтение данных."""
        need_go_to_ch = all([
            model._meta.db_table not in TECH_TABLES,
            model.__name__ in NOT_TECH_MODELS
        ])
        if need_go_to_ch:
            return "clickhouse"

        return 'default'

    def db_for_write(self, model, **hints):
        """Маршрут на запись данных."""
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Разрещение на миграцию."""
        return True
