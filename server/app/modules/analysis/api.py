from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.analysis.repository import get_analysis_result
from app.modules.analysis.schemas import AnalysisResponse
from app.modules.analysis.service import AnalysisService
from app.modules.auth.models import User
from app.modules.claims.repository import get_claim_by_id


router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/{claim_id}", response_model=AnalysisResponse)
def analyze_claim(
    claim_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    claim = get_claim_by_id(db, claim_id=claim_id)

    if claim is None or claim.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Claim not found",
        )

    service = AnalysisService()

    return service.analyze_claim(
        db=db,
        claim_id=claim.id,
        claim_text=claim.claim_text,
    )


@router.get("/{claim_id}", response_model=AnalysisResponse)
def get_analysis(
    claim_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    claim = get_claim_by_id(db, claim_id=claim_id)

    if claim is None or claim.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Claim not found",
        )

    result = get_analysis_result(
        db=db,
        claim_id=claim_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    return result
