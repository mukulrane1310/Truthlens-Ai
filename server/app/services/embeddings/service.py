from sqlalchemy.orm import Session

from app.modules.evidence.models import (
    EvidenceChunk,
    UploadedEvidenceChunk,
)
from app.services.embeddings.fastembed import FastEmbedProvider


class EmbeddingService:

    def __init__(self) -> None:
        self.provider = FastEmbedProvider()

    def embed_evidence_chunks(
        self,
        db: Session,
        chunks: list[EvidenceChunk],
    ) -> None:
        if not chunks:
            return

        texts = [chunk.content for chunk in chunks]
        embeddings = self.provider.embed(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding

        db.commit()

    def embed_uploaded_chunks(
        self,
        db: Session,
        chunks: list[UploadedEvidenceChunk],
    ) -> None:
        if not chunks:
            return

        texts = [chunk.content for chunk in chunks]
        embeddings = self.provider.embed(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding

        db.commit()