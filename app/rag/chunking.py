from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def chunk_text(text: str) -> list[str]:
    """
    Splits raw text into overlapping chunks suitable for embedding.
    Chunk size and overlap are configured via application settings.
    """
    settings = get_settings()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
    )

    chunks = splitter.split_text(text)
    logger.info("Split text into %d chunks (size=%d, overlap=%d)", len(chunks), settings.chunk_size, settings.chunk_overlap)
    return chunks