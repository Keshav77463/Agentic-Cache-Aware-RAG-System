from langchain_chroma import Chroma  # ← new import
from langchain_huggingface import HuggingFaceEmbeddings

def load_vector_store(persist_directory="data/chroma_db"):
    print("Loading embeddings model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("Loading vector database...")
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    print(f"Vector store loaded ✅ — {vector_store._collection.count()} chunks")
    return vector_store