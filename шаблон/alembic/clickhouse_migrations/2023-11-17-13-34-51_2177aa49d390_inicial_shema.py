"""inicial_shema

Revision ID: 2177aa49d390
Revises: 
Create Date: 2023-11-17 13:34:51.730230

"""
from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '2177aa49d390'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    upgrade_clickhouse_migrations()


def downgrade():
    downgrade_clickhouse_migrations()


def upgrade_clickhouse_migrations():
    query = """
    CREATE TABLE test_logs
    (
        id Int32,
        partner_id Int32,
        table String,
        ts_ms DateTime,
        after_data String,
        before_data String,
        op TEXT
    )
    ENGINE = MergeTree
    ORDER BY id
    ;
    """
    connection = op.get_bind()
    connection.execute(text(query))

def downgrade_clickhouse_migrations():
    query = """
        DROP TABLE IF EXISTS test;
    """
    connection = op.get_bind()
    connection.execute(text(query))

