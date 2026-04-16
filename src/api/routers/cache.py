from fastapi import APIRouter
from src.cache.exact_cache import ExactCache
from src.cache.semantic_cache import SemanticCache

router = APIRouter()

exact_cache = ExactCache()
semantic_cache = SemanticCache()

stats = {
    "exact_hits": 0,
    "exact_misses": 0,
    "semantic_hits": 0,
    "semantic_misses": 0
}

@router.get("/cache/stats")
def cache_stats():
    return {
        "exact_cache": {
            "total_keys": len(exact_cache.client.keys("exact:*")),
            "hits": stats["exact_hits"],
            "misses": stats["exact_misses"]
        },
        "semantic_cache": {
            "total_entries": semantic_cache.collection.count(),
            "hits": stats["semantic_hits"],
            "misses": stats["semantic_misses"]
        }
    }

@router.delete("/cache/clear")
def clear_cache():
    exact_cache.clear_all()
    semantic_cache.clear_all()

    # Reset stats too
    stats["exact_hits"] = 0
    stats["exact_misses"] = 0
    stats["semantic_hits"] = 0
    stats["semantic_misses"] = 0

    return {"message": "Both caches cleared "}

@router.delete("/cache/exact")
def clear_exact_cache():
    exact_cache.clear_all()
    stats["exact_hits"] = 0
    stats["exact_misses"] = 0
    return {"message": "Exact cache cleared "}

@router.delete("/cache/semantic")
def clear_semantic_cache():
    semantic_cache.clear_all()
    stats["semantic_hits"] = 0
    stats["semantic_misses"] = 0
    return {"message": "Semantic cache cleared "}