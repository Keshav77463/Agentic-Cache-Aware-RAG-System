from fastapi import APIRouter
from pydantic import BaseModel
import time
from src.pipeline.rag_pipeline import RAGPipeline
from src.cache.exact_cache import ExactCache
from src.cache.semantic_cache import SemanticCache
from src.api.routers.cache import stats

router = APIRouter()

pipeline = RAGPipeline()
exact_cache = ExactCache()
semantic_cache = SemanticCache()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    source: str
    response_time: float

@router.post("/query", response_model=QueryResponse)
def ask(request: QueryRequest):
    query = request.question
    start_time = time.time()

    # Layer 1 — Exact Cache
    answer = exact_cache.get(query)
    if answer:
        stats["exact_hits"] += 1
        return QueryResponse(
            answer=answer,
            source="exact_cache ",
            response_time=round(time.time() - start_time, 4)
        )
    stats["exact_misses"] += 1

    # Layer 2 — Semantic Cache
    answer = semantic_cache.get(query)
    if answer:
        stats["semantic_hits"] += 1
        exact_cache.set(query, answer)
        return QueryResponse(
            answer=answer,
            source="semantic_cache ",
            response_time=round(time.time() - start_time, 4)
        )
    stats["semantic_misses"] += 1


    answer = pipeline._run_rag(query)
    exact_cache.set(query, answer)
    semantic_cache.set(query, answer)

    return QueryResponse(
        answer=answer,
        source="rag ",
        response_time=round(time.time() - start_time, 4)
    )