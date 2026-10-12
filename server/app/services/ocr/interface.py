from abc import ABC, abstractmethod


class OCRProvider(ABC):

    @abstractmethod
    def extract_text(
        self,
        content: bytes,
        filename: str,
    ) -> str:
        """Extract text from an image or scanned document."""
        raise NotImplementedError