from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.chatbot.models import ChatMessage


def create_chat_message(
    db: Session,
    claim_id: UUID,
    role: str,
    content: str,
) -> ChatMessage:
    message = ChatMessage(
        claim_id=claim_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_chat_messages(
    db: Session,
    claim_id: UUID,
) -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.claim_id == claim_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
