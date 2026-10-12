"""add evidence embeddings

Revision ID: 4ce66d3ade63
Revises: 69c2f85d6c84
Create Date: 2026-10-08 16:16:09.467637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "4ce66d3ade63"
down_revision: Union[str, None] = "69c2f85d6c84"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "evidence_chunks",
        sa.Column(
            "embedding",
            Vector(384),
            nullable=True,
        ),
    )

    op.add_column(
        "uploaded_evidence_chunks",
        sa.Column(
            "embedding",
            Vector(384),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "uploaded_evidence_chunks",
        "embedding",
    )

    op.drop_column(
        "evidence_chunks",
        "embedding",
    )
