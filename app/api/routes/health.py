from fastapi import APIRouter

from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health")
async def health():
    logger.info("Health check requested")
    return {
        "status": "healthy"
    }