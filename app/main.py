from fastapi import FastAPI

app = FastAPI(
    title="MedQuery AI API",
    version="1.0.0",
    description="Enterprise Clinical Knowledge Assistant powered by Retrieval-Augmented Generation (RAG)"
)

@app.get("/")
def root():
    return {"message": "Welcome to MedQuery AI"}

@app.get("/health")
def health():
    return {"status": "healthy"}