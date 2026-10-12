from app.services.ocr.interface import OCRProvider


class OCRManager:

    def __init__(
        self,
        provider: OCRProvider,
    ) -> None:
        self.provider = provider

    def extract_text(
        self,
        content: bytes,
        filename: str,
    ) -> str:
        return self.provider.extract_text(
            content=content,
            filename=filename,
        )