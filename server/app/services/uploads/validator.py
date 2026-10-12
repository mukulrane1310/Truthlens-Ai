from pathlib import Path


MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".docx",
}

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

ALLOWED_EXTENSIONS = (
    ALLOWED_DOCUMENT_EXTENSIONS
    | ALLOWED_IMAGE_EXTENSIONS
)


def validate_file_extension(filename: str) -> bool:
    extension = Path(filename).suffix.lower()
    return extension in ALLOWED_EXTENSIONS


def validate_file_size(file_size: int) -> bool:
    return 0 < file_size <= MAX_FILE_SIZE


def validate_upload(
    filename: str,
    file_size: int,
    content_type: str,
) -> bool:
    return (
        validate_file_extension(filename)
        and validate_file_size(file_size)
        and validate_content_type(content_type)
    )

def validate_document_upload(
    filename: str,
    file_size: int,
    content_type: str,
) -> bool:
    extension = Path(filename).suffix.lower()

    return (
        extension in ALLOWED_DOCUMENT_EXTENSIONS
        and validate_file_size(file_size)
        and content_type.lower() in ALLOWED_DOCUMENT_MIME_TYPES
    )


def validate_image_upload(
    filename: str,
    file_size: int,
    content_type: str,
) -> bool:
    extension = Path(filename).suffix.lower()

    return (
        extension in ALLOWED_IMAGE_EXTENSIONS
        and validate_file_size(file_size)
        and content_type.lower() in ALLOWED_IMAGE_MIME_TYPES
    )

ALLOWED_DOCUMENT_MIME_TYPES = {
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

ALLOWED_IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

ALLOWED_MIME_TYPES = (
    ALLOWED_DOCUMENT_MIME_TYPES
    | ALLOWED_IMAGE_MIME_TYPES
)


def validate_content_type(content_type: str) -> bool:
    return content_type.lower() in ALLOWED_MIME_TYPES