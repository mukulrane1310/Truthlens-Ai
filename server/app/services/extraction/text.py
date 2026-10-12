def extract_text_from_txt(content: bytes) -> str:
    if not content:
        raise ValueError("File is empty")

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Invalid UTF-8 text file") from exc

    text = text.strip()

    if not text:
        raise ValueError("File contains no text")

    return text