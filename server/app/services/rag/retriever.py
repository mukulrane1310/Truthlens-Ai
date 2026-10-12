from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.evidence.repository import (
    get_source_by_id,
    get_uploaded_source_by_id,
)
from app.services.rag.interface import (
    RAGRetriever,
    RetrievedEvidence,
)
from app.services.retrieval.service import RetrievalService


class EvidenceRAGRetriever(RAGRetriever):

    def __init__(self) -> None:
        self.retrieval_service = RetrievalService()

    def retrieve(
        self,
        claim_id: UUID,
        query: str,
        top_k: int = 5,
        db: Session | None = None,
    ) -> list[RetrievedEvidence]:

        if db is None:
            raise ValueError("Database session is required")

        web_chunks = self.retrieval_service.retrieve_web_evidence(
            db=db,
            claim_id=claim_id,
            query=query,
            top_k=top_k,
        )

        uploaded_chunks = (
            self.retrieval_service.retrieve_uploaded_evidence(
                db=db,
                claim_id=claim_id,
                query=query,
                top_k=top_k,
            )
        )

        results: list[RetrievedEvidence] = []

        for chunk in web_chunks:
            source = get_source_by_id(
                db=db,
                source_id=chunk.source_id,
            )

            if source is None:
                continue

            results.append(
                RetrievedEvidence(
                    id=chunk.id,
                    content=chunk.content,
                    source_id=chunk.source_id,
                    source_url=source.url,
                    source_title=source.title,
                    source_type=source.source_type,
                )
            )

        for chunk in uploaded_chunks:
            source = get_uploaded_source_by_id(
                db=db,
                source_id=chunk.uploaded_source_id,
            )

            if source is None:
                continue

            results.append(
                RetrievedEvidence(
                    id=chunk.id,
                    content=chunk.content,
                    source_id=chunk.uploaded_source_id,
                    source_url=None,
                    source_title=source.filename,
                    source_type=source.source_type,
                )
            )

        return results
