"""Claims API routes — all require authentication."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.claims import service
from app.modules.claims.schemas import ClaimCreate, ClaimListResponse, ClaimResponse

router = APIRouter(prefix="/claims", tags=["Claims"])


@router.post("", response_model=ClaimResponse, status_code=201)
def create_claim(
    data: ClaimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_claim(db, user_id=current_user.id, data=data)


@router.get("", response_model=ClaimListResponse)
def list_claims(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.list_claims(db, user_id=current_user.id, limit=limit, offset=offset)


@router.get("/{claim_id}", response_model=ClaimResponse)
def get_claim(
    claim_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_claim(db, claim_id=claim_id, user_id=current_user.id)
