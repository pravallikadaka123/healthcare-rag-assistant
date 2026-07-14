import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from fastapi import UploadFile

from app.core.config import get_settings
from app.core.logging import get_logger
from app.rag.chunking import chunk_text
from app.rag.text_extraction import TextExtractionError, extract_text_from_pdf

logger = get_logger(__name__)


class DocumentProcessingError(Exception):
    """Raised when a document fails to process end-to-end."""


@dataclass
class DocumentProcessingResult:
    filename: str
    page_count: int
    chunk_count: int
    chunks: list[str]


def _save_upload(file: UploadFile) -> Path:
    settings = get_settings()
    documents_dir = Path(settings.documents_dir)
    documents_dir.mkdir(parents=True, exist_ok=True)

    # Prefix with a UUID to avoid filename collisions between uploads
    safe_name = f"{uuid.uuid4().hex}_{file.filename}"
    destination = documents_dir / safe_name

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info("Saved uploaded file to %s", destination)
    return destination


def process_document(file: UploadFile) -> DocumentProcessingResult:
    """
    Orchestrates the full document processing pipeline:
    save -> extract text -> chunk.
    """
    if file.content_type != "application/pdf":
        raise DocumentProcessingError(f"Unsupported file type: {file.content_type}. Only PDF is supported.")

    file_path = _save_upload(file)

    try:
        text, page_count = extract_text_from_pdf(file_path)
    except TextExtractionError as exc:
        raise DocumentProcessingError(str(exc)) from exc

    chunks = chunk_text(text)

    return DocumentProcessingResult(
        filename=file.filename,
        page_count=page_count,
        chunk_count=len(chunks),
        chunks=chunks,
    )