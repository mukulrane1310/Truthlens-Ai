from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.evidence.models import (
    EvidenceChunk,
    UploadedEvidenceChunk,
)
from app.modules.evidence.repository import (
    search_similar_evidence_chunks,
    search_similar_uploaded_chunks,
)
from app.services.embeddings.fastembed import FastEmbedProvider


class RetrievalService:

    def __init__(self) -> None:
        self.embedding_provider = FastEmbedProvider()

    def retrieve_web_evidence(
        self,
        db: Session,
        claim_id: UUID,
        query: str,
        top_k: int = 5,
    ) -> list[EvidenceChunk]:
        embeddings = self.embedding_provider.embed([query])

        if not embeddings:
            return []

        return search_similar_evidence_chunks(
            db=db,
            claim_id=claim_id,
            embedding=embeddings[0],
            top_k=top_k,
        )

    def retrieve_uploaded_evidence(
        self,
        db: Session,
        claim_id: UUID,
        query: str,
        top_k: int = 5,
    ) -> list[UploadedEvidenceChunk]:
        embeddings = self.embedding_provider.embed([query])

        if not embeddings:
            return []

        return search_similar_uploaded_chunks(
            db=db,
            claim_id=claim_id,
            embedding=embeddings[0],
            top_k=top_k,
        )
