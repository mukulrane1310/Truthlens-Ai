from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.services.llm.schemas import (
    EvidenceAssessment,
    Verdict,
)


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    claim_id: UUID
    verdict: Verdict
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str
    evidence: list[EvidenceAssessment]
    created_at: datetime
