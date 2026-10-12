from io import BytesIO

from docx import Document


def extract_text_from_docx(content: bytes) -> str:
    if not content:
        raise ValueError("File is empty")

    try:
        document = Document(BytesIO(content))
    except Exception as exc:
        raise ValueError("Invalid DOCX file") from exc

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    extracted_text = "\n\n".join(paragraphs).strip()

    if not extracted_text:
        raise ValueError("DOCX contains no extractable text")

    return extracted_text