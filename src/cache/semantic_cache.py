import numpy as np
import json
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings

class SemanticCache:
    def __init__(self, threshold=0.75):
        self.client = chromadb.PersistentClient(path="./data/chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="semantic_cache",
            metadata={"hnsw:space": "cosine"}
        )
        self.threshold = threshold
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

    def get(self, query):
        query_vec = self.embedding_model.embed_query(query)

        print(f"[SemanticCache] Collection count: {self.collection.count()}")

        results = self.collection.query(
            query_embeddings=[query_vec],
            n_results=1
        )

        print(f"[SemanticCache] Results: {results}")

        if not results["ids"][0]:
            print("[SemanticCache] MISS (empty)")
            return None

        score = 1 - results["distances"][0][0]
        print(f"[SemanticCache] Score: {score:.2f}")

        if score >= self.threshold:
            print(f"[SemanticCache] HIT (similarity={score:.2f})")
            return json.loads(results["documents"][0][0])

        print(f"[SemanticCache] MISS (similarity={score:.2f})")
        return None

    def set(self, query, answer):
        query_vec = self.embedding_model.embed_query(query)
        self.collection.add(
            ids=[str(hash(query))],
            embeddings=[query_vec],
            documents=[json.dumps(answer)],
            metadatas=[{"query": query}]
        )
        print("[SemanticCache] Saved to cache 💾")

    def clear_all(self):
        self.client.delete_collection("semantic_cache")
        print("[SemanticCache] Cache cleared 🧹")