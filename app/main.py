from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(
        "Starting %s v%s [environment=%s, debug=%s]",
        settings.app_name,
        settings.app_version,
        settings.environment,
        settings.debug,
    )
    yield
    # Shutdown
    logger.info("Shutting down %s", settings.app_name)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    lifespan=lifespan,
)

app.include_router(api_router ,prefix=settings.api_v1_prefix)

@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
    }