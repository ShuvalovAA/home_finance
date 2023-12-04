"""Хранилище коннекторов к базам данных."""

__all__ = [
    'ConnectorsStorage',
]


class ConnectorsStorage:
    def __init__(self, pg_connector, ch_connector, redis_connector, partner_id):
        self.pg_connector = pg_connector
        self.ch_connector = ch_connector
        self.redis_connector = redis_connector
        self.partner_id = partner_id
