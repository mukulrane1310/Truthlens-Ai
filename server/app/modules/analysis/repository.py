from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.analysis.models import AnalysisResult


def create_analysis_result(
    db: Session,
    claim_id: UUID,
    verdict: str,
    confidence: float,
    summary: str,
    evidence: list,
) -> AnalysisResult:
    result = AnalysisResult(
        claim_id=claim_id,
        verdict=verdict,
        confidence=confidence,
        summary=summary,
        evidence=evidence,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result


def get_analysis_result(
    db: Session,
    claim_id: UUID,
) -> AnalysisResult | None:
    return (
        db.query(AnalysisResult)
        .filter(AnalysisResult.claim_id == claim_id)
        .order_by(AnalysisResult.created_at.desc())
        .first()
    )
