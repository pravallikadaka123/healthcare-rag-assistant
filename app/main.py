from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    logger.info(
        "Starting %s v%s [environment=%s, debug=%s]",
        settings.app_name,
        settings.app_version,
        settings.environment,
        settings.debug,
    )


@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
    }