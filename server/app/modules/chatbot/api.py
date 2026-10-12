from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.modules.auth.models import User
from app.modules.chatbot.repository import get_chat_messages
from app.modules.chatbot.schemas import (
    ChatHistoryResponse,
    ChatMessageResponse,
    ChatRequest,
)
from app.modules.chatbot.service import ChatbotService
from app.modules.claims.repository import get_claim_by_id


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "/{claim_id}",
    response_model=ChatMessageResponse,
)
def chat(
    claim_id: UUID,
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    claim = get_claim_by_id(db, claim_id=claim_id)

    if claim is None or claim.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Claim not found",
        )

    _, assistant_message = ChatbotService().chat(
        db=db,
        claim_id=claim.id,
        claim_text=claim.claim_text,
        message=data.message,
    )

    return assistant_message


@router.get(
    "/{claim_id}",
    response_model=ChatHistoryResponse,
)
def get_chat_history(
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

    messages = get_chat_messages(
        db=db,
        claim_id=claim_id,
    )

    return ChatHistoryResponse(
        messages=messages,
    )
