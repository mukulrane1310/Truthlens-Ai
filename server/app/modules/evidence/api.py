from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.claims import service as claims_service
from app.modules.evidence.schemas import (
    EvidenceChunkResponse,
    EvidenceCollectRequest,
    SourceResponse,
)
from app.modules.evidence.service import (
    collect_evidence,
    get_claim_chunks,
    get_claim_evidence,
)
from app.services.search.tavily import TavilySearchProvider
from app.modules.evidence.schemas import (
    UploadedEvidenceListResponse,
)
from app.modules.claims import service as claims_service
from app.modules.evidence import service as evidence_service


router = APIRouter(prefix="/evidence", tags=["Evidence"])


@router.post(
    "/collect/{claim_id}",
    response_model=list[SourceResponse],
)
def collect_claim_evidence(
    claim_id: UUID,
    payload: EvidenceCollectRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    claim = claims_service.get_claim(
        db=db,
        claim_id=str(claim_id),
        user_id=current_user.id,
    )

    provider = TavilySearchProvider()

    return collect_evidence(
        db=db,
        claim_id=claim.id,
        query=payload.query,
        search_provider=provider,
        max_results=payload.max_results,
    )


@router.get(
    "/{claim_id}",
    response_model=list[SourceResponse],
)
def get_evidence(
    claim_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    claim = claims_service.get_claim(
        db=db,
        claim_id=str(claim_id),
        user_id=current_user.id,
    )

    return get_claim_evidence(
        db=db,
        claim_id=claim.id,
    )

@router.get(
    "/{claim_id}/chunks",
    response_model=list[EvidenceChunkResponse],
)
def get_evidence_chunks(
    claim_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    claim = claims_service.get_claim(
        db=db,
        claim_id=str(claim_id),
        user_id=current_user.id,
    )

    return get_claim_chunks(
        db=db,
        claim_id=claim.id,
    )

@router.get(
    "/{claim_id}/uploaded",
    response_model=UploadedEvidenceListResponse,
    status_code=status.HTTP_200_OK,
)
def get_uploaded_evidence(
    claim_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    claims_service.get_claim(
        db=db,
        claim_id=str(claim_id),
        user_id=current_user.id,
    )

    sources = evidence_service.get_uploaded_claim_evidence(
        db=db,
        claim_id=claim_id,
    )

    chunks = evidence_service.get_uploaded_claim_chunks(
        db=db,
        claim_id=claim_id,
    )

    return {
        "sources": sources,
        "chunks": chunks,
    }