import chromadb
import redis

# Use absolute path
client = chromadb.PersistentClient(path="D:/Agentic/data/chroma_db")

try:
    client.delete_collection("semantic_cache")
    print("Semantic cache cleared ")
except Exception as e:
    print(f"Error: {e}")

# Verify
import sqlite3
conn = sqlite3.connect("D:/Agentic/data/chroma_db/chroma.sqlite3")
cursor = conn.cursor()
cursor.execute("SELECT id, name FROM collections")
rows = cursor.fetchall()
print("Remaining collections:", rows)
conn.close()

# Clear Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
keys = r.keys("exact:*")
for key in keys:
    r.delete(key)
print(f"Redis cleared — {len(keys)} keys deleted ")