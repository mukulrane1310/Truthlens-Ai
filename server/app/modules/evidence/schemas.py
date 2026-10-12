from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EvidenceCollectRequest(BaseModel):
    query: str
    max_results: int = 5


class SourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    claim_id: UUID
    url: str
    title: str
    content: str
    source_type: str
    published_date: datetime | None
    author: str | None
    created_at: datetime


class EvidenceChunkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_id: UUID
    claim_id: UUID
    chunk_index: int
    content: str
    created_at: datetime


class UploadedSourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    claim_id: UUID
    filename: str
    content_type: str
    source_type: str
    content: str
    created_at: datetime


class UploadedEvidenceChunkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    uploaded_source_id: UUID
    claim_id: UUID
    chunk_index: int
    content: str
    created_at: datetime

class UploadedEvidenceResponse(BaseModel):
    source: UploadedSourceResponse
    chunks: list[UploadedEvidenceChunkResponse]

class UploadedEvidenceListResponse(BaseModel):
    sources: list[UploadedSourceResponse]
    chunks: list[UploadedEvidenceChunkResponse]
