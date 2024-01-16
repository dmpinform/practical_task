from functools import partial

from alembic import context
from reports.adapters.database.tables import metadata_app
from sqlalchemy import create_engine, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata_app

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        include_schemas=True,
        version_table_schema=target_metadata.schema,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    def check_schema(object, name, type_, reflected, compare_to, db_schema):
        return type_ == 'table' and object.schema == db_schema

    def include_name(name, type_, parent_names):
        if type_ == 'schema':
            return name in [target_metadata.schema]
        else:
            return True

    connectable = create_engine(
        config.get_main_option('sqlalchemy.url'), poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=partial(
                check_schema, db_schema=target_metadata.schema
            ),
            version_table_schema=target_metadata.schema,
            include_name=include_name,
            compare_type=True,
        )

        with context.begin_transaction():
            schema_exists = connection.execute(
                'select exists (select schema_name '
                'from information_schema.schemata '
                f"where schema_name = '{target_metadata.schema}');"
            ).scalar()
            if not schema_exists:
                connection.execute(f'create schema {target_metadata.schema};')
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
