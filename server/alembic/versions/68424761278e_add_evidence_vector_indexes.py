"""add evidence vector indexes

Revision ID: 68424761278e
Revises: 4ce66d3ade63
"""

from typing import Sequence, Union

from alembic import op


revision: str = "68424761278e"
down_revision: Union[str, None] = "4ce66d3ade63"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_evidence_chunks_embedding_hnsw",
        "evidence_chunks",
        ["embedding"],
        unique=False,
        postgresql_using="hnsw",
        postgresql_ops={
            "embedding": "vector_cosine_ops",
        },
    )

    op.create_index(
        "ix_uploaded_evidence_chunks_embedding_hnsw",
        "uploaded_evidence_chunks",
        ["embedding"],
        unique=False,
        postgresql_using="hnsw",
        postgresql_ops={
            "embedding": "vector_cosine_ops",
        },
    )


def downgrade() -> None:
    op.drop_index(
        "ix_uploaded_evidence_chunks_embedding_hnsw",
        table_name="uploaded_evidence_chunks",
    )

    op.drop_index(
        "ix_evidence_chunks_embedding_hnsw",
        table_name="evidence_chunks",
    )
