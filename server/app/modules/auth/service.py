"""Auth service — business logic on top of the repository."""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.modules.auth import repository
from app.modules.auth.models import User
from app.modules.auth.schemas import LoginRequest, RegisterRequest, TokenResponse


def register_user(db: Session, data: RegisterRequest) -> User:
    email = data.email.lower()
    if repository.get_user_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    hashed = hash_password(data.password)
    return repository.create_user(db, email=email, hashed_password=hashed)


def login_user(db: Session, data: LoginRequest) -> TokenResponse:
    email = data.email.lower()
    user = repository.get_user_by_email(db, email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)
