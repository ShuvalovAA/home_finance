import logging
from logging.config import fileConfig
import re
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool, func, Column
from sqlalchemy.ext.declarative import declarative_base
from clickhouse_sqlalchemy.alembic.dialect import include_object as include_object_clickhouse
from clickhouse_sqlalchemy import engines, types

from alembic import context

USE_TWOPHASE = False

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# gather section names referring to different
# databases.  These are named "engine1", "engine2"
# in the sample .ini file.
db_names = config.get_main_option("databases")

# add your model's MetaData objects here
# for 'autogenerate' support.  These must be set
# up to hold just those tables targeting a
# particular database. table.tometadata() may be
# helpful here in case a "copy" of
# a MetaData is needed.
# from myapp import mymodel
# target_metadata = {
#       'engine1':mymodel.metadata1,
#       'engine2':mymodel.metadata2
# }

Base = declarative_base()
target_metadata = {
    'postgresql_migrations': Base.metadata,
    'clickhouse_migrations': Base.metadata
}

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# задать подключения через окружение
# export STAGING_SQLALCHEMY_DATABASE_URI=postgresql://postgres:1@localhost:5432/postgres
db_env_var_prefix_dict = {
    'postgresql_migrations': 'POSTGRESQL_',
    'clickhouse_migrations': 'CLICKHOUSE_'
}


def _build_url(prefix):
    url = ''
    user = os.environ.get(f'CHANGESET_{prefix}USER')
    password = os.environ.get(f'CHANGESET_{prefix}PASSWORD')
    host = os.environ.get(f'CHANGESET_{prefix}HOST')
    port = os.environ.get(f'CHANGESET_{prefix}PORT')
    db = os.environ.get(f'CHANGESET_{prefix}DATABASE')

    if prefix == 'POSTGRESQL_':
        url = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
            user=user,
            password=password,
            host=host,
            port=port,
            db=db
        )
    if prefix == 'CLICKHOUSE_':
        url = 'clickhouse://{user}:{password}@{host}/{db}'.format(
            user=user,
            password=password,
            host=host,
            db=db
        )

    return url


for db_name, prefix in db_env_var_prefix_dict.items():
    url = _build_url(prefix)
    config.set_section_option(
        db_name,
        'sqlalchemy.url',
        url
    )


def _patch_alembic_version_for_ch(context, **kwargs):
    migration_context = context._proxy._migration_context
    version = migration_context._version

    dt = Column('dt', types.DateTime, server_default=func.now())
    version.append_column(dt)
    version.engine = engines.ReplacingMergeTree(
        version=dt, order_by=func.tuple()
    )


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # for the --sql use case, run migrations for each URL into
    # individual files.

    engines = {}
    for name in re.split(r",\s*", db_names):
        engines[name] = rec = {}
        rec["url"] = context.config.get_section_option(name, "sqlalchemy.url")

    for name, rec in engines.items():
        logger.info(f"Migrating database {name}")
        file_ = f"{name}.sql"
        logger.info(f"Writing output to {file_}")
        with open(file_, "w") as buffer:
            context.configure(
                url=rec["url"],
                output_buffer=buffer,
                target_metadata=target_metadata.get(name),
                literal_binds=True,
                dialect_opts={"paramstyle": "named"},
            )
            with context.begin_transaction():
                context.run_migrations(engine_name=name)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    is_clickhouse = config.config_ini_section == "clickhouse_migrations"

    config_section = config.get_section(config.config_ini_section)
    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    target_metadata_for_pg = [metadata for _, metadata in target_metadata.items() if _ == "postgresql_migrations"]
    target_metadata_for_ch = [metadata for _, metadata in target_metadata.items() if _ == "clickhouse_migrations"]
    version_table = config_section.get('version_table')

    def include_object(object, name, type_, reflected, compare_to):
        if type_ == 'foreign_key_constraint' and compare_to and (
                compare_to.elements[0].target_fullname == db_name + '.' +
                object.elements[0].target_fullname or
                db_name + '.' + compare_to.elements[0].target_fullname == object.elements[
                    0].target_fullname):
            return False
        if type_ == 'table':
            if object.schema == db_name or object.schema is None:
                return True
        elif object.table.schema == db_name or object.table.schema is None:
            return True
        else:
            return False

    i_o = include_object_clickhouse if is_clickhouse else include_object
    target_md = target_metadata_for_ch if is_clickhouse else target_metadata_for_pg

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_md, include_object=i_o,
            version_table=version_table
        )

        with context.begin_transaction():
            if is_clickhouse:
                _patch_alembic_version_for_ch(context)
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
