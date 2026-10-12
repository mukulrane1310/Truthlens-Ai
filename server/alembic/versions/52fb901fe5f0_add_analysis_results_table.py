"""add analysis results table

Revision ID: 52fb901fe5f0
Revises: 68424761278e
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "52fb901fe5f0"
down_revision: Union[str, None] = "68424761278e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "analysis_results",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("claim_id", sa.UUID(), nullable=False),
        sa.Column("verdict", sa.String(length=50), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["claim_id"],
            ["claims.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_analysis_results_claim_id",
        "analysis_results",
        ["claim_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_analysis_results_claim_id",
        table_name="analysis_results",
    )
    op.drop_table("analysis_results")
