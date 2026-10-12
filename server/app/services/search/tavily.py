from tavily import TavilyClient

from app.core.config import settings
from app.services.search.interface import SearchProvider, SearchResult


class TavilySearchProvider(SearchProvider):

    def __init__(self) -> None:
        self.client = TavilyClient(
            api_key=settings.TAVILY_API_KEY
        )

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:
        response = self.client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=False,
            include_raw_content=True,
        )

        return [
            SearchResult(
                title=result.get("title", ""),
                url=result.get("url", ""),
                content=(
                    result.get("raw_content")
                    or result.get("content", "")
                ),
                published_date=result.get("published_date"),
                author=result.get("author"),
            )
            for result in response.get("results", [])
        ]