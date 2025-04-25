import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Import your database Base
from app.database import Base  

# ✅ Import ALL models to register metadata
# from app.model import user, patient, staff, appointment, payment, medicine, prescription, report

# ✅ Set target metadata
target_metadata = Base.metadata

# ✅ Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Configure Alembic to use the correct database URL
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ✅ Logging setup
if config.config_file_name:
    fileConfig(config.config_file_name)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()