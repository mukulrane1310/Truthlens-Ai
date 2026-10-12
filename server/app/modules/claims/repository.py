"""Claims repository — raw DB queries."""
import uuid

from sqlalchemy.orm import Session

from app.modules.claims.models import Claim


def create_claim(db: Session, user_id: uuid.UUID, claim_text: str) -> Claim:
    claim = Claim(user_id=user_id, claim_text=claim_text)
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


def get_claims_by_user(
    db: Session, user_id: uuid.UUID, limit: int, offset: int
) -> tuple[list[Claim], int]:
    q = db.query(Claim).filter(Claim.user_id == user_id)
    total = q.count()
    items = q.order_by(Claim.created_at.desc()).offset(offset).limit(limit).all()
    return items, total


def get_claim_by_id(db: Session, claim_id: str | uuid.UUID) -> Claim | None:
    if isinstance(claim_id, str):
        try:
            claim_id = uuid.UUID(claim_id)
        except ValueError:
            return None
    return db.query(Claim).filter(Claim.id == claim_id).first()
