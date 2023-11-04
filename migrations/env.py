import os
import sys
from logging.config import fileConfig

import sqlalchemy as sa
from alembic import context, op
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import engine_from_config, pool

import src.models.model as models
from src.core.config import DATABASE_URL
from src.db.db_setup import engine

# access to the values within the .ini file
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = models.Base.metadata

mig_con = MigrationContext.configure(engine.connect())
oparations = Operations(mig_con)


def upgrade():
    oparations.create_table(
        'urls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_url', sa.String(), nullable=False),
        sa.Column('short_url_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('deleted', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    oparations.create_table(
        'url_access',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url_id', sa.Integer(), nullable=False),
        sa.Column('access_time', sa.DateTime(), nullable=False),
        sa.Column('user_agent', sa.String(), nullable=False),
        sa.Column('client_ip', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['url_id'], ['urls.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    oparations.drop_table('url_access')
    oparations.drop_table('urls')


def migrate_offline() -> None:
    """Run migrations in 'offline' mode.

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


def migrate_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    migrate_offline()
else:
    upgrade()
    migrate_online()
