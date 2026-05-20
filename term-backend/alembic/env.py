# -*- coding: utf-8 -*-
# mypy: ignore-errors
# isort:skip_file
# pylint: skip-file
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from service.database.common import BaseTable
from service.database.models.users import User, UserGroup, Group
from service.database.models.building_project import BuildingInfo
from service.settings import Settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config_file_name = config.config_file_name
if not config_file_name:
    raise ValueError(f"There is no config file name")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config_file_name)

settings = Settings()
config.set_main_option("sqlalchemy.url", settings.POSTGRES_SERVERS.unicode_string())

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = BaseTable.metadata

__tables__ = (
    User,
    UserGroup,
    Group,
    BuildingInfo,
)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: AsyncConnection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
