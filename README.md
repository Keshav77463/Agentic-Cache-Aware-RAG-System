# 🧠 Agentic Cache-Aware RAG System

An intelligent **Retrieval-Augmented Generation (RAG)** pipeline with **multi-layer caching** and **smart query routing** — designed to drastically reduce LLM latency and API costs while maintaining answer quality.

Built on Amazon Fine Food Reviews data with **50,000 sampled reviews**.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Layer Caching** | 3-tier lookup: Exact → Semantic → Full RAG |
| **Exact Cache (Redis)** | Sub-millisecond lookups via MD5-hashed query keys with TTL auto-expiry |
| **Semantic Cache (ChromaDB)** | Cosine-similarity matching to serve answers for *semantically similar* queries |
| **Cache Promotion** | Semantic cache hits get promoted to Redis for faster repeat access |
| **FastAPI Backend** | RESTful API with query, health, and cache management endpoints |
| **Streamlit Dashboard** | Interactive chat UI with real-time cache monitoring sidebar |
| **Groq LLM (Llama 3.1 8B)** | Ultra-fast inference via Groq's hardware-accelerated API |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Groq Cloud — `llama-3.1-8b-instant` |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` |
| **Vector Store** | ChromaDB (persistent, cosine similarity) |
| **Exact Cache** | Redis (MD5-keyed, 1-hour TTL) |
| **Orchestration** | LangChain |
| **API** | FastAPI |
| **Frontend** | Streamlit |
| **Data** | Amazon Fine Food Reviews (50K sample) |
| **Package Manager** | uv |

---

## 📁 Project Structure

```
Agentic-Cache-Aware-RAG-System/
├── main.py                        # CLI entry point (interactive REPL)
├── streamlit.py                   # Streamlit chat UI with cache monitor
├── pyproject.toml                 # Dependencies & project metadata
├── .env                           # Environment variables (GROQ_API_KEY)
│
├── src/
│   ├── api/
│   │   ├── app.py                 # FastAPI application factory
│   │   └── routers/
│   │       ├── query.py           # POST /query — main RAG endpoint
│   │       ├── cache.py           # GET/DELETE /cache/* — cache management
│   │       └── health.py          # GET /health — health check
│   │
│   ├── cache/
│   │   ├── exact_cache.py         # Redis-based exact match cache
│   │   ├── semantic_cache.py      # ChromaDB-based semantic similarity cache
│   │   └── clear_cache.py         # Standalone cache clearing utility
│   │
│   ├── embeddings/
│   │   └── embedder.py            # Vector store creation from text chunks
│   │
│   ├── llm/
│   │   └── generator.py           # Groq LLM initialization
│   │
│   ├── pipeline/
│   │   └── rag_pipeline.py        # Core 3-layer RAG pipeline orchestrator
│   │
│   ├── retriever/
│   │   └── vector_store.py        # ChromaDB vector store loader
│   │
│   └── utils/
│       └── chunking.py            # Sliding-window text chunker
│
├── notebook/
│   └── data_preprocessing.py      # Data cleaning & sampling script
│
└── data/
    ├── Reviews.csv                # Raw Amazon reviews dataset
    ├── cleaned_reviews.csv        # Preprocessed reviews (50K sample)
    └── chroma_db/                 # Persisted ChromaDB vector store
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** ≥ 3.11
- **Redis** server running on `localhost:6379`
- **Groq API Key** — get one at [console.groq.com](https://console.groq.com)
- **uv** (recommended) or pip

### 1. Clone the Repository

```bash
git clone https://github.com/Keshav77463/Agentic-Cache-Aware-RAG-System.git
cd Agentic-Cache-Aware-RAG-System
```

### 2. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Start Redis

```bash
# macOS (Homebrew)
brew services start redis

# Linux
sudo systemctl start redis

# Windows (WSL or Docker)
docker run -d -p 6379:6379 redis
```

### 5. Prepare the Data

Run the preprocessing script to clean and sample the reviews:

```bash
cd notebook
python data_preprocessing.py
```

> **Note:** The raw `Reviews.csv` (~300MB) is expected in the `data/` directory. You can download it from the [Amazon Fine Food Reviews dataset on Kaggle](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews).

---

## 💡 Usage

### Option A: CLI Interface

```bash
python main.py
```

```
Enter your query: What do people think about the coffee?
Final Answer: Based on the reviews, customers generally find...
```

### Option B: FastAPI + Streamlit (Full Stack)

**Terminal 1 — Start the API server:**

```bash
uvicorn src.api.app:app --reload
```

**Terminal 2 — Start the Streamlit UI:**

```bash
streamlit run streamlit.py
```

Open [http://localhost:8501](http://localhost:8501) to use the chat interface with the live cache monitor.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/query` | Submit a question (returns answer, source, response time) |
| `GET` | `/cache/stats` | View cache hit/miss statistics |
| `DELETE` | `/cache/clear` | Clear both Redis & Semantic caches |
| `DELETE` | `/cache/exact` | Clear Redis exact cache only |
| `DELETE` | `/cache/semantic` | Clear ChromaDB semantic cache only |

### Example Request

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What do customers say about the taste of coffee?"}'
```

### Example Response

```json
{
  "answer": "Based on the reviews, customers generally...",
  "source": "rag",
  "response_time": 2.3451
}
```

---

## ⚡ How the Caching Works

```
Query arrives
    │
    ├─→ Layer 1: Exact Cache (Redis)
    │     • Normalizes query (lowercase + strip)
    │     • MD5 hash → Redis key lookup
    │     • TTL: 1 hour auto-expiry
    │     • ⚡ ~1ms latency
    │
    ├─→ Layer 2: Semantic Cache (ChromaDB)
    │     • Embeds query with all-MiniLM-L6-v2
    │     • Cosine similarity search (threshold ≥ 0.75)
    │     • Hit → promotes answer to Redis for next time
    │     • 🧠 ~50-100ms latency
    │
    └─→ Layer 3: Full RAG Pipeline
          • Retrieves top-10 document chunks from ChromaDB
          • Sends context + query to Groq (Llama 3.1 8B)
          • Caches result in both Redis and Semantic Cache
          • 🌐 ~1-3s latency
```

---

## 🔧 Configuration

| Parameter | Location | Default | Description |
|-----------|----------|---------|-------------|
| `GROQ_API_KEY` | `.env` | — | Your Groq API key |
| Redis host/port | `exact_cache.py` | `localhost:6379` | Redis connection |
| Redis TTL | `exact_cache.py` | `3600` (1 hour) | Cache expiry time |
| Semantic threshold | `semantic_cache.py` | `0.75` | Min cosine similarity for a hit |
| Top-K retrieval | `rag_pipeline.py` | `10` | Number of chunks retrieved |
| Chunk size | `chunking.py` | `100` words | Sliding window chunk size |
| Chunk overlap | `chunking.py` | `20` words | Overlap between chunks |
| LLM model | `generator.py` | `llama-3.1-8b-instant` | Groq model name |
| LLM temperature | `generator.py` | `0` | Deterministic output |

---

## 📊 Performance Comparison

| Source | Typical Latency | API Cost |
|--------|----------------|----------|
| Exact Cache (Redis) | ~1 ms | $0 |
| Semantic Cache | ~50-100 ms | $0 |
| Full RAG | ~1-3 s | Groq API tokens |

> Repeated and semantically similar queries are served **100-1000x faster** from cache, with **zero additional LLM cost**.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📬 Contact

**Keshav** — [GitHub](https://github.com/Keshav77463)
