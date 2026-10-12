from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SearchResult:
    title: str
    url: str
    content: str
    published_date: str | None = None
    author: str | None = None


class SearchProvider(ABC):

    @abstractmethod
    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:
        """Search for web evidence."""
        raise NotImplementedError
