from fastembed import TextEmbedding

from app.services.embeddings.interface import EmbeddingProvider


class FastEmbedProvider(EmbeddingProvider):

    def __init__(self) -> None:
        self.model = TextEmbedding()

    def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self.model.embed(texts)

        return [
            embedding.tolist()
            for embedding in embeddings
        ]