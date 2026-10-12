from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.evidence.models import (
    EvidenceChunk,
    Source,
    UploadedEvidenceChunk,
    UploadedSource,
)


def create_source(
    db: Session,
    claim_id: UUID,
    url: str,
    title: str,
    content: str,
    source_type: str = "WEB",
    published_date=None,
    author: str | None = None,
) -> Source:
    source = Source(
        claim_id=claim_id,
        url=url,
        title=title,
        content=content,
        source_type=source_type,
        published_date=published_date,
        author=author,
    )

    db.add(source)
    db.flush()
    db.refresh(source)

    return source


def get_sources_by_claim(
    db: Session,
    claim_id: UUID,
) -> list[Source]:
    return (
        db.query(Source)
        .filter(Source.claim_id == claim_id)
        .order_by(Source.created_at.desc())
        .all()
    )


def get_chunks_by_claim(
    db: Session,
    claim_id: UUID,
) -> list[EvidenceChunk]:
    return (
        db.query(EvidenceChunk)
        .filter(EvidenceChunk.claim_id == claim_id)
        .order_by(
            EvidenceChunk.source_id,
            EvidenceChunk.chunk_index,
        )
        .all()
    )


def create_uploaded_source(
    db: Session,
    claim_id: UUID,
    filename: str,
    content_type: str,
    source_type: str,
    content: str,
) -> UploadedSource:
    source = UploadedSource(
        claim_id=claim_id,
        filename=filename,
        content_type=content_type,
        source_type=source_type,
        content=content,
    )

    db.add(source)
    db.flush()
    db.refresh(source)

    return source


def create_uploaded_evidence_chunk(
    db: Session,
    uploaded_source_id: UUID,
    claim_id: UUID,
    chunk_index: int,
    content: str,
) -> UploadedEvidenceChunk:
    chunk = UploadedEvidenceChunk(
        uploaded_source_id=uploaded_source_id,
        claim_id=claim_id,
        chunk_index=chunk_index,
        content=content,
    )

    db.add(chunk)
    db.flush()
    db.refresh(chunk)

    return chunk


def get_uploaded_sources_by_claim(
    db: Session,
    claim_id: UUID,
) -> list[UploadedSource]:
    return (
        db.query(UploadedSource)
        .filter(UploadedSource.claim_id == claim_id)
        .order_by(UploadedSource.created_at.desc())
        .all()
    )


def get_uploaded_chunks_by_claim(
    db: Session,
    claim_id: UUID,
) -> list[UploadedEvidenceChunk]:
    return (
        db.query(UploadedEvidenceChunk)
        .filter(
            UploadedEvidenceChunk.claim_id == claim_id
        )
        .order_by(
            UploadedEvidenceChunk.uploaded_source_id,
            UploadedEvidenceChunk.chunk_index,
        )
        .all()
    )

def search_similar_evidence_chunks(
    db: Session,
    claim_id: UUID,
    embedding: list[float],
    top_k: int = 5,
) -> list[EvidenceChunk]:
    return (
        db.query(EvidenceChunk)
        .filter(
            EvidenceChunk.claim_id == claim_id,
            EvidenceChunk.embedding.is_not(None),
        )
        .order_by(
            EvidenceChunk.embedding.cosine_distance(embedding)
        )
        .limit(top_k)
        .all()
    )


def search_similar_uploaded_chunks(
    db: Session,
    claim_id: UUID,
    embedding: list[float],
    top_k: int = 5,
) -> list[UploadedEvidenceChunk]:
    return (
        db.query(UploadedEvidenceChunk)
        .filter(
            UploadedEvidenceChunk.claim_id == claim_id,
            UploadedEvidenceChunk.embedding.is_not(None),
        )
        .order_by(
            UploadedEvidenceChunk.embedding.cosine_distance(
                embedding
            )
        )
        .limit(top_k)
        .all()
    )


def get_source_by_id(
    db: Session,
    source_id: UUID,
) -> Source | None:
    return (
        db.query(Source)
        .filter(Source.id == source_id)
        .first()
    )


def get_uploaded_source_by_id(
    db: Session,
    source_id: UUID,
) -> UploadedSource | None:
    return (
        db.query(UploadedSource)
        .filter(UploadedSource.id == source_id)
        .first()
    )
