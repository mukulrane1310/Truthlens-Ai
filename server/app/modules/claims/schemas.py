
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator

_MIN_LEN = 10
_MAX_LEN = 1000

# Request

class ClaimCreate(BaseModel):
    claim_text: str

    @field_validator("claim_text")
    @classmethod
    def clean_claim(cls, v: str) -> str:
        import re
        v = re.sub(r"\s+", " ", v.strip())
        if len(v) < _MIN_LEN:
            raise ValueError(f"Claim must be at least {_MIN_LEN} characters")
        if len(v) > _MAX_LEN:
            raise ValueError(f"Claim must be at most {_MAX_LEN} characters")
        return v


# Response

class ClaimResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    claim_text: str
    claim_type: str
    entities: list[Any]
    keywords: list[Any]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ClaimListResponse(BaseModel):
    items: list[ClaimResponse]
    total: int
    limit: int
    offset: int
