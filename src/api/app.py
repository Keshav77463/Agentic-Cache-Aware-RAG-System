

from fastapi import FastAPI
from src.api.routers import health, cache, query


app = FastAPI(
    title="Agentic Cache-Aware RAG",
    description="RAG pipeline with multi-layer caching",
    version="1.0.0"
)


app.include_router(health.router)
app.include_router(cache.router)
app.include_router(query.router)