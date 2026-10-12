"""Alembic env.py - reads DATABASE_URL from pydantic settings."""
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.database import Base, engine
from app.core.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

import app.modules.auth.models  # noqa: F401
import app.modules.claims.models  # noqa: F401
import app.modules.evidence.models  # noqa: F401
import app.modules.analysis.models  # noqa: F401
import app.modules.chatbot.models  # noqa: F401

target_metadata = Base.metadata


HNSW_INDEXES = {
    "ix_evidence_chunks_embedding_hnsw",
    "ix_uploaded_evidence_chunks_embedding_hnsw",
}


def include_object(
    object,
    name,
    type_,
    reflected,
    compare_to,
):
    if type_ == "index" and name in HNSW_INDEXES:
        return False

    return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
