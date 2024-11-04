from django.core.management.base import BaseCommand
from django.db import connections
from root.management.tools_bar.clickhouse.match_pg_ch_types import MATTCHING_FIELDS_TYPES

'''to delete
на мастере
CREATE PUBLICATION my_publication FOR ALL TABLES;

на реплике
CREATE SUBSCRIPTION my_subscription  CONNECTION 'host=hfin-postgresql-master port=6432 dbname=postgres password=postgres' PUBLICATION publication_for_slaves;
'''


class Command(BaseCommand):
    """Команда настраивает логическую репликацию между инстансами PostgreSQL.

    Сценарий команды забирает все соединения где имя совмпадает с подстрокой 'postgresql_replica' из пула
    конфигурации root.settings.DATABASES

    WARNING: комнда должна быть выполнена после проведения миграций на всех базах postgresql.
    REQUAREMENT:
     - /etc/postgesql/postgresql.conf должен содержать wal_level=logical
     - /etc/postgesql/postgresql.conf должен содержать max_replication_slots=20
     - /etc/postgesql/postgresql.conf должен содержать max_logical_replication_workers=10
     - /etc/postgesql/postgresql.conf должен содержать max_worker_processes=13
    """
    help = "Команда создаёт публикацию WAL в мастере и подписку в slave"
    PUBLITION_NAME = 'publication_for_slaves'

    def _set_publication_master(self, pg_connection):
        query = f'''
            CREATE PUBLICATION 
                {self.PUBLITION_NAME}
            FOR ALL TABLES;
        '''
        with pg_connection.cursor() as cursor:
            cursor.execute(query)

    def _set_subcription_slave(self, pg_connection, pg_replica_connection):
        query = '''
            CREATE SUBSCRIPTION 
                subscription_{alias}
            CONNECTION 
                'host={host} port={port} dbname={db_name} password={password} user={user}'
            PUBLICATION {publication_master};    
        '''.format(
            alias=pg_replica_connection.alias,
            host=pg_connection.settings_dict['HOST'],
            port=pg_connection.settings_dict['PORT'],
            db_name=pg_connection.settings_dict['NAME'],
            password=pg_connection.settings_dict['PASSWORD'],
            user=pg_connection.settings_dict['USER'],
            publication_master=self.PUBLITION_NAME
        )
        with pg_replica_connection.cursor() as cursor:
            cursor.execute(query)

    def add_arguments(self, parser):
        "Добавление аргументов из треминальной строки"
        pass

    def handle(self, *args, **options):
        pg_connection = connections['default']
        self._set_publication_master(pg_connection=pg_connection)
        pg_replica_connections_name = [name for name in connections if 'postgresql_replica' in name]
        pg_replica_connections = [connections[name] for name in pg_replica_connections_name]
        for pg_replica_connection in pg_replica_connections:
            self._set_subcription_slave(pg_connection=pg_connection, pg_replica_connection=pg_replica_connection)
            print(f'Logical Replication set on:\t {pg_replica_connection.alias}')
