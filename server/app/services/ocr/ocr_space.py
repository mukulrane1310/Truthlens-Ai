import requests

from app.core.config import settings
from app.services.ocr.interface import OCRProvider


OCR_API_URL = "https://api.ocr.space/parse/image"


class OCRSpaceProvider(OCRProvider):

    def extract_text(
        self,
        content: bytes,
        filename: str,
    ) -> str:
        response = requests.post(
            OCR_API_URL,
            files={
                "file": (
                    filename,
                    content,
                ),
            },
            data={
                "apikey": settings.OCR_SPACE_API_KEY,
                "language": "eng",
                "isOverlayRequired": "false",
                "OCREngine": "2",
            },
            timeout=30,
        )

        response.raise_for_status()

        result = response.json()

        if result.get("IsErroredOnProcessing"):
            raise ValueError(
                "OCR processing failed"
            )

        parsed_results = result.get(
            "ParsedResults",
            [],
        )

        text_parts = [
            item.get("ParsedText", "").strip()
            for item in parsed_results
            if item.get("ParsedText", "").strip()
        ]

        text = "\n\n".join(text_parts).strip()

        if not text:
            raise ValueError(
                "OCR returned no extractable text"
            )

        return text