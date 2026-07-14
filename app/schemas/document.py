from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    """Response returned after a document has been processed."""

    filename: str = Field(..., description="Original filename of the uploaded document")
    page_count: int = Field(..., description="Number of pages extracted from the PDF")
    chunk_count: int = Field(..., description="Number of text chunks generated")
    chunks: list[str] = Field(..., description="The extracted text chunks")


class DocumentUploadError(BaseModel):
    """Standard error response for document upload failures."""

    detail: str