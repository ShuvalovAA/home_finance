"""inicial_shema

Revision ID: d6d5c623b4f5
Revises: 
Create Date: 2023-11-17 09:55:11.191410

"""
from alembic import op
from sqlalchemy import text
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '486748302250'
down_revision = None
branch_labels = None
depends_on = None

conn = op.get_bind()
inspector = Inspector.from_engine(conn)
tables = inspector.get_table_names()
indexes = []
for table in tables:
    table_indexes = inspector.get_indexes(table)
    for index in table_indexes:
        indexes.append(
            index.get('name')
        )


def upgrade():
    upgrade_postgresql_migrations()


def downgrade():
    downgrade_postgresql_migrations()


def upgrade_postgresql_migrations():
    if 'multipart_upload' not in tables:
        connection = op.get_bind()
        query = """
            CREATE TABLE multipart_upload(
                id serial,
                partner_id int NOT NULL,
                status int NOT NULL,
                target_table text NOT NULL,
                start_date timestamp WITH TIME ZONE NOT NULL,
                period_start timestamp WITH TIME ZONE NOT NULL,
                period_end timestamp WITH TIME ZONE NOT NULL,
                parts_count int,
                storage_key text,
                multipart_id text,
                msg_abort text
            );
            CREATE TABLE uploading_parts(
                id serial,
                process_id int NOT NULL,
                status int NOT NULL,
                start_date timestamp WITH TIME ZONE NOT NULL,
                part_position int NOT NULL,
                etag text
            );
        """
        connection.execute(text(query))


def downgrade_postgresql_migrations():
    if 'multipart_upload' in tables:
        op.drop_table('multipart_upload')
    if 'uploading_parts' in tables:
        op.drop_table('uploading_parts')

