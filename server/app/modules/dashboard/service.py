from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.dashboard.repository import (
    count_analyses,
    count_claims,
    count_uploaded_sources,
    count_web_sources,
    get_verdict_counts,
)
from app.modules.dashboard.schemas import DashboardSummary, VerdictStats


class DashboardService:
    def get_summary(
        self,
        db: Session,
        user_id: UUID,
    ) -> DashboardSummary:
        verdict_counts = get_verdict_counts(
            db=db,
            user_id=user_id,
        )

        return DashboardSummary(
            total_claims=count_claims(
                db=db,
                user_id=user_id,
            ),
            total_analyses=count_analyses(
                db=db,
                user_id=user_id,
            ),
            total_web_sources=count_web_sources(
                db=db,
                user_id=user_id,
            ),
            total_uploaded_sources=count_uploaded_sources(
                db=db,
                user_id=user_id,
            ),
            verdicts=VerdictStats(
                supported=verdict_counts.get("SUPPORTED", 0),
                partially_supported=verdict_counts.get(
                    "PARTIALLY_SUPPORTED", 0
                ),
                mixed_evidence=verdict_counts.get(
                    "MIXED_EVIDENCE", 0
                ),
                not_supported=verdict_counts.get(
                    "NOT_SUPPORTED", 0
                ),
                insufficient_evidence=verdict_counts.get(
                    "INSUFFICIENT_EVIDENCE", 0
                ),
            ),
        )
