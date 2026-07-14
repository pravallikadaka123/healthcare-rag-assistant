from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="MedQuery AI API",
    version="1.0.0",
    description="Enterprise Clinical Knowledge Assistant powered by Retrieval-Augmented Generation (RAG)"
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "application": "MedQuery AI",
        "version": "1.0.0",
        "status": "running"
    }