"""enable analysis results rls

Revision ID: 620d2f33292d
Revises: 52fb901fe5f0
"""

from typing import Sequence, Union

from alembic import op


revision: str = "620d2f33292d"
down_revision: Union[str, None] = "52fb901fe5f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE public.analysis_results ENABLE ROW LEVEL SECURITY"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE public.analysis_results DISABLE ROW LEVEL SECURITY"
    )