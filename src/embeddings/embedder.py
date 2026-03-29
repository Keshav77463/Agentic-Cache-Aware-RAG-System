from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

def create_vectorstore(chunks,persist_directory="data/chroma_db"):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
    )

    docs = []
    for chunk in chunks:

        doc = Document(page_content=chunk)
        docs.append(doc)
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory,
    )
    print('vector store created')
    return vector_store

