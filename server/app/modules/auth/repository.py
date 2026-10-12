import uuid

from sqlalchemy.orm import Session

from app.modules.auth.models import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str | uuid.UUID) -> User | None:
    if isinstance(user_id, str):
        try:
            user_id = uuid.UUID(user_id)
        except ValueError:
            return None
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, email: str, hashed_password: str) -> User:
    user = User(email=email, hashed_password=hashed_password, role="USER")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
