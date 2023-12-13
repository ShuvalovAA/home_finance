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
    rows = []
    for i in range(1, 150001, 1):
        row = (
            i,
           3000,
           "table_name1",
           "2023-03-01",
           json.dumps({"id": i, "first_name": f"Foo{i}"}),
           json.dumps({"id": i, "first_name": f"Bar{i}"}),
           "u"
        )
        rows.append(row)

    rows_str = ','.join([str(r) for r in rows])
    query = """
        insert into 
        test_logs (id, partner_id, table, operation_date, after_data, before_data, operation_type)
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

