from fastapi import APIRouter, HTTPException, UploadFile

from app.core.logging import get_logger
from app.schemas.document import DocumentUploadResponse
from app.services.document_service import DocumentProcessingError, process_document

router = APIRouter()
logger = get_logger(__name__)


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile):
    logger.info("Received upload request for %s", file.filename)

    try:
        result = process_document(file)
    except DocumentProcessingError as exc:
        logger.warning("Document processing failed for %s: %s", file.filename, exc)
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return DocumentUploadResponse(
        filename=result.filename,
        page_count=result.page_count,
        chunk_count=result.chunk_count,
        chunks=result.chunks,
    )