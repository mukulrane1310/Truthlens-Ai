from io import BytesIO

from pypdf import PdfReader


def extract_text_from_pdf(content: bytes) -> str:
    if not content:
        raise ValueError("File is empty")

    try:
        reader = PdfReader(BytesIO(content))
    except Exception as exc:
        raise ValueError("Invalid PDF file") from exc

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""

        if text.strip():
            pages.append(text.strip())

    extracted_text = "\n\n".join(pages).strip()

    if not extracted_text:
        raise ValueError("PDF contains no extractable text")

    return extracted_text