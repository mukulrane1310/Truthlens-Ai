
from functools import lru_cache

from fastembed import TextEmbedding

from app.services.embeddings.interface import EmbeddingProvider

MODEL_NAME = "BAAI/bge-small-en-v1.5"  # 384 dimensions, matches Vector(384)


@lru_cache(maxsize=1)
def _get_model() -> TextEmbedding:
    return TextEmbedding(MODEL_NAME)


class FastEmbedProvider(EmbeddingProvider):

    def __init__(self) -> None:
        self.model = _get_model()

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        return [e.tolist() for e in self.model.embed(texts)]
