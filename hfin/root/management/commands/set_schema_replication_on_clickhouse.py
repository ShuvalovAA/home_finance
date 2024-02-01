from django.core.management.base import BaseCommand
from django.db import connections
from root.management.tools_bar.clickhouse.match_pg_ch_types import MATTCHING_FIELDS_TYPES
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Команда настраивает схему данных clickhouse на репликацию из postgresql-master.

    WARNING: комнда должна быть выполнена после проведения миграций на всех базах.connection.
    REQUAREMENT:
     - /etc/postgesql/postgresql.conf должен содержать wal_level=logical
     - /etc/postgesql/postgresql.conf должен содержать max_replication_slots=20
     - /etc/postgesql/postgresql.conf должен содержать max_logical_replication_workers=10
     - /etc/postgesql/postgresql.conf должен содержать max_worker_processes = 13
    """
    help = "Команда создаёт в инстантсе clickhouse таблицы с движками MaterializedPostgreSQL"

    def _generate_table_fields_str(self, table_fields):
        result = ''
        table_fields_str_list = []
        for field in table_fields:
            field_type = MATTCHING_FIELDS_TYPES[field[1]]
            field_str = ' '.join([field[0], field_type])
            table_fields_str_list.append(field_str)
        result = ', '.join(table_fields_str_list)
        return result

    def _set_materialized_in_clickhouse(self, table_name, table_fields, pg_connection):
        table_fields_str = self._generate_table_fields_str(table_fields=table_fields)
        query = '''
            CREATE TABLE {table_name} ({table_fields})
            ENGINE = MaterializedPostgreSQL('{pg_host}:{pg_port}', '{pg_db_name}', '{table_name_replica}', '{pg_user}', '{pg_password}')
            PRIMARY KEY {key};
        '''.format(
            table_name=table_name,
            table_name_replica=table_name,
            table_fields=table_fields_str,
            key=table_fields[0][0],
            pg_host=pg_connection.settings_dict['HOST'],
            pg_port=pg_connection.settings_dict['PORT'],
            pg_db_name=pg_connection.settings_dict['NAME'],
            pg_user=pg_connection.settings_dict['USER'],
            pg_password=pg_connection.settings_dict['PASSWORD']
        )

        with connections['clickhouse'].cursor() as cursor:
            try:
                cursor.execute(query)
            except OperationalError as error_operation:
                error = error_operation
                if error.args[0].code == 57:
                    print(error)

    def _get_all_info_from_master(self, pg_connection):
        query = '''
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE 
            substring(TABLE_NAME, 'pg') IS NULL
            AND substring(TABLE_NAME, 'postgresql') IS NULL
            AND table_schema = 'public';
        '''
        with pg_connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def add_arguments(self, parser):
        "Добавление аргументов из треминальной строки"
        pass

    def handle(self, *args, **options):
        pg_connection = connections['default']
        all_tables_info = self._get_all_info_from_master(pg_connection)
        tables = set([r[0] for r in all_tables_info])
        for table in tables:
            table_fields = [(r[1], r[2]) for r in all_tables_info if r[0] == table]
            self._set_materialized_in_clickhouse(
                table_name=table,
                table_fields=table_fields,
                pg_connection=pg_connection
            )
