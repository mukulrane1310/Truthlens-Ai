import re
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.evidence.models import (
    EvidenceChunk,
)
from app.modules.evidence.repository import (
    create_source,
    get_sources_by_claim,
    get_chunks_by_claim,
    create_uploaded_source,
    create_uploaded_evidence_chunk,
    get_uploaded_sources_by_claim,
    get_uploaded_chunks_by_claim,
)
from app.services.embeddings.service import EmbeddingService
from app.services.extraction.url_validator import is_safe_url
from app.services.rag.chunker import chunk_text
from app.services.search.interface import SearchProvider


def clean_text(value: str) -> str:
    if not value:
        return ""

    # Remove embedded base64 images and image placeholders.
    value = re.sub(
        r"!\[[^\]]*\]\(\s*data:image/[^)]*\)",
        " ",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"data:image/[^;\s]+;base64,[A-Za-z0-9+/=\s]+",
        " ",
        value,
        flags=re.IGNORECASE,
    )

    # Remove HTML image tags and remaining HTML markup.
    value = re.sub(r"<img\b[^>]*>", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", " ", value)

    # Remove Markdown links while retaining their visible text.
    value = re.sub(r"\[([^\]]+)\]\((?:[^()]|\([^()]*\))*\)", r"\1", value)

    # Remove standalone Markdown image syntax.
    value = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", value)

    # Remove common page-navigation and promotional phrases.
    value = re.sub(
        r"\b(?:accessibility statement|share this article|"
        r"share this page|subscribe to our newsletter)\b",
        " ",
        value,
        flags=re.IGNORECASE,
    )

    # Normalize whitespace.
    return " ".join(value.split())


def create_evidence_chunks(
    db: Session,
    source_id: UUID,
    claim_id: UUID,
    content: str,
):
    chunks = chunk_text(content)

    evidence_chunks = []

    for index, chunk in enumerate(chunks):
        evidence_chunk = EvidenceChunk(
            source_id=source_id,
            claim_id=claim_id,
            chunk_index=index,
            content=chunk,
        )

        db.add(evidence_chunk)
        evidence_chunks.append(evidence_chunk)

    db.flush()

    return evidence_chunks


def collect_evidence(
    db: Session,
    claim_id: UUID,
    query: str,
    search_provider: SearchProvider,
    max_results: int = 5,
):
    results = search_provider.search(
        query=query,
        max_results=max_results,
    )

    existing_sources = get_sources_by_claim(
        db=db,
        claim_id=claim_id,
    )

    existing_urls = {
        source.url
        for source in existing_sources
    }

    seen_urls = set()
    sources = []

    for result in results:
        url = result.url

        if not is_safe_url(url):
            continue

        if url in seen_urls or url in existing_urls:
            continue

        title = clean_text(result.title)
        content = clean_text(result.content)

        if not title or not content:
            continue

        seen_urls.add(url)

        source = create_source(
            db=db,
            claim_id=claim_id,
            url=url,
            title=title,
            content=content,
            published_date=result.published_date,
            author=result.author,
        )

        chunks = create_evidence_chunks(
            db=db,
            source_id=source.id,
            claim_id=claim_id,
            content=content,
        )

        EmbeddingService().embed_evidence_chunks(
            db=db,
            chunks=chunks,
        )

        sources.append(source)

    db.commit()

    return sources


def get_claim_evidence(
    db: Session,
    claim_id: UUID,
):
    return get_sources_by_claim(
        db=db,
        claim_id=claim_id,
    )


def get_claim_chunks(
    db: Session,
    claim_id: UUID,
):
    return get_chunks_by_claim(
        db=db,
        claim_id=claim_id,
    )


def create_uploaded_evidence(
    db: Session,
    claim_id: UUID,
    filename: str,
    content_type: str,
    source_type: str,
    content: str,
):
    content = clean_text(content)

    if not content:
        raise ValueError(
            "Uploaded file contains no extractable text"
        )

    source = create_uploaded_source(
        db=db,
        claim_id=claim_id,
        filename=filename,
        content_type=content_type,
        source_type=source_type,
        content=content,
    )

    chunks = chunk_text(content)

    evidence_chunks = []

    for index, chunk in enumerate(chunks):
        evidence_chunks.append(
            create_uploaded_evidence_chunk(
                db=db,
                uploaded_source_id=source.id,
                claim_id=claim_id,
                chunk_index=index,
                content=chunk,
            )
        )

    db.flush()

    EmbeddingService().embed_uploaded_chunks(
        db=db,
        chunks=evidence_chunks,
    )

    db.commit()

    return source, evidence_chunks


def get_uploaded_claim_evidence(
    db: Session,
    claim_id: UUID,
):
    return get_uploaded_sources_by_claim(
        db=db,
        claim_id=claim_id,
    )


def get_uploaded_claim_chunks(
    db: Session,
    claim_id: UUID,
):
    return get_uploaded_chunks_by_claim(
        db=db,
        claim_id=claim_id,
    )