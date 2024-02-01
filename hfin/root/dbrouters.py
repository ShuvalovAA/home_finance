class DBRouter:
    """Маршрутизатор запросов к базам данных."""
    def __init__(self):
        pass

    def db_for_read(self, model, **hints):
        return "clickhouse"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
