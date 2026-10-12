from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass
class RetrievedEvidence:
    id: UUID
    content: str
    source_id: UUID
    source_url: str | None
    source_title: str | None
    source_type: str


class RAGRetriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        claim_id: UUID,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedEvidence]:
        """Retrieve relevant evidence for a claim."""
        raise NotImplementedError
