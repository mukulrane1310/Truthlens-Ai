"""Claims service — business logic."""
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.claims import repository
from app.modules.claims.models import Claim
from app.modules.claims.schemas import ClaimCreate, ClaimListResponse, ClaimResponse


def create_claim(db: Session, user_id: uuid.UUID, data: ClaimCreate) -> Claim:
    """Create a new claim for *user_id*."""
    return repository.create_claim(db, user_id=user_id, claim_text=data.claim_text)


def list_claims(
    db: Session, user_id: uuid.UUID, limit: int, offset: int
) -> ClaimListResponse:
    items, total = repository.get_claims_by_user(db, user_id, limit, offset)
    return ClaimListResponse(
        items=[ClaimResponse.model_validate(c) for c in items],
        total=total,
        limit=limit,
        offset=offset,
    )


def get_claim(db: Session, claim_id: str, user_id: uuid.UUID) -> Claim:
    claim = repository.get_claim_by_id(db, claim_id)
    if claim is None or claim.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")
    return claim
