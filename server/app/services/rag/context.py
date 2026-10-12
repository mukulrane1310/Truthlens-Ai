from dataclasses import dataclass

from app.services.rag.interface import RetrievedEvidence


@dataclass
class RAGContextItem:
    citation_id: str
    content: str
    source_title: str | None
    source_url: str | None
    source_type: str


class RAGContextBuilder:

    MAX_ITEMS = 10
    MAX_CHARS_PER_ITEM = 2000
    MAX_TOTAL_CHARS = 12000

    def build(
        self,
        evidence: list[RetrievedEvidence],
    ) -> list[RAGContextItem]:

        items: list[RAGContextItem] = []
        seen_content: set[str] = set()
        total_chars = 0

        for item in evidence:
            content = item.content.strip()

            if not content or content in seen_content:
                continue

            content = content[: self.MAX_CHARS_PER_ITEM]

            if total_chars + len(content) > self.MAX_TOTAL_CHARS:
                break

            if len(items) >= self.MAX_ITEMS:
                break

            seen_content.add(content)

            items.append(
                RAGContextItem(
                    citation_id=f"E{len(items) + 1}",
                    content=content,
                    source_title=item.source_title,
                    source_url=item.source_url,
                    source_type=item.source_type,
                )
            )

            total_chars += len(content)

        return items

    def format_for_llm(
        self,
        items: list[RAGContextItem],
    ) -> str:
        if not items:
            return ""

        sections: list[str] = []

        for item in items:
            source = item.source_title or "Unknown source"
            url = item.source_url or "N/A"

            sections.append(
                f"[{item.citation_id}]\n"
                f"Source: {source}\n"
                f"URL: {url}\n"
                f"Type: {item.source_type}\n"
                f"Evidence:\n{item.content}"
            )

        return "\n\n".join(sections)
