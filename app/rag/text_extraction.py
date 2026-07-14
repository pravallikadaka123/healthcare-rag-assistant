from pathlib import Path

from pypdf import PdfReader

from app.core.logging import get_logger

logger = get_logger(__name__)


class TextExtractionError(Exception):
    """Raised when text cannot be extracted from a document."""


def extract_text_from_pdf(file_path: Path) -> tuple[str, int]:
    """
    Extracts raw text from a PDF file.

    Returns:
        A tuple of (full_text, page_count).

    Raises:
        TextExtractionError: if the file can't be read or contains no extractable text.
    """
    try:
        reader = PdfReader(str(file_path))
    except Exception as exc:
        logger.error("Failed to open PDF %s: %s", file_path, exc)
        raise TextExtractionError(f"Could not open PDF: {exc}") from exc

    page_count = len(reader.pages)
    text_parts: list[str] = []

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
        except Exception as exc:
            logger.warning("Failed to extract text from page %d: %s", page_number, exc)

    full_text = "\n".join(text_parts).strip()

    if not full_text:
        raise TextExtractionError(
            "No extractable text found in PDF (it may be scanned/image-based)."
        )

    logger.info("Extracted %d characters from %d pages in %s", len(full_text), page_count, file_path.name)
    return full_text, page_count