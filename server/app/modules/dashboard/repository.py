from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.analysis.models import AnalysisResult
from app.modules.claims.models import Claim
from app.modules.evidence.models import Source, UploadedSource


def count_claims(
    db: Session,
    user_id: UUID,
) -> int:
    return (
        db.query(func.count(Claim.id))
        .filter(Claim.user_id == user_id)
        .scalar()
        or 0
    )


def count_analyses(
    db: Session,
    user_id: UUID,
) -> int:
    return (
        db.query(func.count(AnalysisResult.id))
        .join(Claim, AnalysisResult.claim_id == Claim.id)
        .filter(Claim.user_id == user_id)
        .scalar()
        or 0
    )


def count_web_sources(
    db: Session,
    user_id: UUID,
) -> int:
    return (
        db.query(func.count(Source.id))
        .join(Claim, Source.claim_id == Claim.id)
        .filter(Claim.user_id == user_id)
        .scalar()
        or 0
    )


def count_uploaded_sources(
    db: Session,
    user_id: UUID,
) -> int:
    return (
        db.query(func.count(UploadedSource.id))
        .join(Claim, UploadedSource.claim_id == Claim.id)
        .filter(Claim.user_id == user_id)
        .scalar()
        or 0
    )


def get_verdict_counts(
    db: Session,
    user_id: UUID,
) -> dict[str, int]:
    rows = (
        db.query(
            AnalysisResult.verdict,
            func.count(AnalysisResult.id),
        )
        .join(Claim, AnalysisResult.claim_id == Claim.id)
        .filter(Claim.user_id == user_id)
        .group_by(AnalysisResult.verdict)
        .all()
    )

    return {
        verdict: count
        for verdict, count in rows
    }
