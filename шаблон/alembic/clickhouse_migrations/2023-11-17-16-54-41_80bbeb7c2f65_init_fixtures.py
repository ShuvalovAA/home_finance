"""init_fixtures

Revision ID: 80bbeb7c2f65
Revises: 2177aa49d390
Create Date: 2023-11-17 16:54:41.881222

"""
from alembic import op
from sqlalchemy import text
import json


# revision identifiers, used by Alembic.
revision = '80bbeb7c2f65'
down_revision = '2177aa49d390'
branch_labels = None
depends_on = None


def upgrade():
    upgrade_clickhouse_migrations()


def downgrade():
    downgrade_clickhouse_migrations()


def upgrade_clickhouse_migrations():

    rows = [
        (1,
         2014,
         'table_name1',
         '2023-03-01',
         json.dumps({"id": 1, "first_name": "Foo1"}),
         json.dumps({"id": 1, "first_name": "Bar1"}),
         'u'
         ),
        (2,
         2014,
         'table_name1',
         '2023-03-01',
         json.dumps({"id": 2, "first_name": "Foo2"}),
         json.dumps({"id": 2, "first_name": "Bar2"}),
         'u'
         ),
        (3,
         2014,
         'table_name1',
         '2023-03-01',
         json.dumps({"id": 3, "first_name": "Foo3"}),
         json.dumps({"id": 3, "first_name": "Bar3"}),
         'u'
         )
    ]

    rows_str = ','.join([str(r) for r in rows])
    query = """
        insert test_logs
          test (id, table, ts_ms, after_data, before_data, op)
        VALUES
          {rows}
          ;
    """.format(rows=rows_str)
    connection = op.get_bind()
    connection.execute(text(query))


def downgrade_clickhouse_migrations():
    query = """
        TRUNCATE TABLE IF EXISTS "test";
    """
    connection = op.get_bind()
    connection.execute(text(query))

