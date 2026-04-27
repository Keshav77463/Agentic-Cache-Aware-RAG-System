import streamlit as st
import requests

# ─────────────────────────────────
# Page config
# ─────────────────────────────────
st.set_page_config(
    page_title="Agentic Cache-Aware RAG",
    page_icon="🧠",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# ─────────────────────────────────
# Title
# ─────────────────────────────────
st.title("🧠 Agentic Cache-Aware RAG")
st.caption("Multi-layer caching with Exact + Semantic + RAG pipeline")

# ─────────────────────────────────
# Sidebar
# ─────────────────────────────────
with st.sidebar:
    st.header("⚡ Cache Monitor")
    st.divider()

    try:
        stats = requests.get(f"{API_URL}/cache/stats").json()

        st.subheader("🔴 Exact Cache (Redis)")
        col1, col2, col3 = st.columns(3)
        col1.metric("Keys", stats["exact_cache"]["total_keys"])
        col2.metric("Hits", stats["exact_cache"]["hits"])
        col3.metric("Misses", stats["exact_cache"]["misses"])

        st.divider()

        st.subheader("🟣 Semantic Cache (ChromaDB)")
        col4, col5, col6 = st.columns(3)
        col4.metric("Entries", stats["semantic_cache"]["total_entries"])
        col5.metric("Hits", stats["semantic_cache"]["hits"])
        col6.metric("Misses", stats["semantic_cache"]["misses"])

    except:
        st.error("❌ Cannot connect to FastAPI")

    st.divider()

    st.subheader("🧹 Clear Cache")
    if st.button("Clear Both Caches", use_container_width=True):
        requests.delete(f"{API_URL}/cache/clear")
        st.success("Both caches cleared ✅")
        st.rerun()

    col7, col8 = st.columns(2)
    with col7:
        if st.button("Clear Redis", use_container_width=True):
            requests.delete(f"{API_URL}/cache/exact")
            st.success("Redis cleared ")
            st.rerun()
    with col8:
        if st.button("Clear ChromaDB", use_container_width=True):
            requests.delete(f"{API_URL}/cache/semantic")
            st.success("ChromaDB cleared ")
            st.rerun()

# ─────────────────────────────────
# Chat history
# ─────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "metadata" in message:
            col1, col2 = st.columns(2)
            col1.caption(f"⚡ Source: {message['metadata']['source']}")
            col2.caption(f"⏱ Time: {message['metadata']['response_time']}s")

# ─────────────────────────────────
# Chat input
# ─────────────────────────────────
if query := st.chat_input("Ask a question about the reviews..."):

    with st.chat_message("user"):
        st.write(query)
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.spinner("Thinking..."):
        response = requests.post(
            f"{API_URL}/query",
            json={"question": query}
        ).json()

    with st.chat_message("assistant"):
        st.write(response["answer"])
        col1, col2 = st.columns(2)
        col1.caption(f"⚡ Source: {response['source']}")
        col2.caption(f"⏱ Time: {response['response_time']}s")

    st.session_state.messages.append({
        "role": "assistant",
        "content": response["answer"],
        "metadata": {
            "source": response["source"],
            "response_time": response["response_time"]
        }
    })

    st.rerun()