from src.utils.chunking import chunk_text
import pandas as pd
from src.embeddings.embedder import create_vectorstore

# load correct file
df = pd.read_csv("data/cleaned_reviews.csv")

all_chunks = []

# chunking
for text in df['text']:
    chunks = chunk_text(text)
    all_chunks.extend(chunks)

print("Total chunks:", len(all_chunks))
print(all_chunks[:5])

# ✅ pass chunks (NOT full text)
vector_store = create_vectorstore(all_chunks)

print("Vector store created successfully")