from fastapi import UploadFile

from app.services.extraction.docx import extract_text_from_docx
from app.services.extraction.pdf import extract_text_from_pdf
from app.services.extraction.text import extract_text_from_txt
from app.services.ocr.manager import OCRManager
from app.services.ocr.ocr_space import OCRSpaceProvider
from app.services.uploads.validator import (
    validate_document_upload,
    validate_image_upload,
)


async def validate_uploaded_file(
    file: UploadFile,
    upload_type: str,
) -> bytes:
    content = await file.read()

    if not file.filename:
        raise ValueError("Filename is required")

    if upload_type == "document":
        is_valid = validate_document_upload(
            filename=file.filename,
            file_size=len(content),
            content_type=file.content_type or "",
        )
    elif upload_type == "image":
        is_valid = validate_image_upload(
            filename=file.filename,
            file_size=len(content),
            content_type=file.content_type or "",
        )
    else:
        raise ValueError("Invalid upload type")

    if not is_valid:
        raise ValueError("Invalid file")

    return content


async def extract_uploaded_text(
    file: UploadFile,
    upload_type: str,
) -> str:
    content = await validate_uploaded_file(
        file,
        upload_type,
    )

    filename = (file.filename or "").lower()

    if upload_type == "image":
        ocr_manager = OCRManager(
            provider=OCRSpaceProvider(),
        )

        return ocr_manager.extract_text(
            content=content,
            filename=file.filename or "image.png",
        )

    if upload_type != "document":
        raise ValueError("Invalid upload type")

    if filename.endswith(".txt"):
        return extract_text_from_txt(content)

    if filename.endswith(".pdf"):
        try:
            return extract_text_from_pdf(content)
        except ValueError as exc:
            if str(exc) != "PDF contains no extractable text":
                raise

        ocr_manager = OCRManager(
            provider=OCRSpaceProvider(),
        )

        return ocr_manager.extract_text(
            content=content,
            filename=file.filename or "document.pdf",
        )

    if filename.endswith(".docx"):
        return extract_text_from_docx(content)

    raise ValueError(
        "Text extraction currently supports "
        "TXT, PDF, and DOCX files only"
    )