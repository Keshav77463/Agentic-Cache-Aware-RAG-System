from src.retriever.vector_store import load_vector_store
from src.llm.generator import get_llm
from src.cache.exact_cache import ExactCache
from src.cache.semantic_cache import SemanticCache


class RAGPipeline:
    def __init__(self):
        print("Initializing RAG Pipeline...")
        self.retriever = load_vector_store().as_retriever(search_kwargs={"k": 10})
        self.llm = get_llm()
        self.exact_cache = ExactCache()
        self.semantic_cache = SemanticCache()
        print("RAG Pipeline ready ")

    def run(self, query: str) -> str:

        # Layer 1 — Exact Cache (Redis) ⚡ fastest
        answer = self.exact_cache.get(query)
        if answer:
            print("Exact Cache HIT ⚡")
            return answer

        # Layer 2 — Semantic Cache (ChromaDB) 🧠 smart
        answer = self.semantic_cache.get(query)
        if answer:
            print("Semantic Cache HIT ")
            self.exact_cache.set(query, answer)  # promote to Redis
            return answer

        # Layer 3 — Full RAG
        print("Cache MISS — Running full RAG...")
        answer = self._run_rag(query)

        # Save to both caches
        self.exact_cache.set(query, answer)
        self.semantic_cache.set(query, answer)

        return answer

    def _run_rag(self, query: str) -> str:
        # Step 1 — Retrieve relevant docs
        docs = self.retriever.invoke(query)

        if not docs:
            return " No documents found. Please run ingestion first."

        # Step 2 — Build context from retrieved chunks
        context = "\n".join([doc.page_content for doc in docs])

        # Step 3 — Call LLM
        response = self.llm.invoke(f"""
        Answer using only the context below.

        Context:
        {context}

        Question:
        {query}
        """)

        return response.content