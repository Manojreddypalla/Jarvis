# tools/rag_agent_tools.py

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_qdrant import QdrantVectorStore


# ---------------- CONFIG ----------------

QDRANT_URL = "http://localhost:6333"
COLLECTION = "learning_rag"

EMBED_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama3"

BASE_URL = "http://localhost:11434"


# ---------------- INDEX ----------------

def index_pdf(file_path: str):

    path = Path(file_path)

    if not path.exists():
        return f"❌ File not found: {file_path}"


    loader = PyPDFLoader(str(path))
    docs = loader.load()


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)


    embedder = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=BASE_URL
    )


    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedder,
        url=QDRANT_URL,
        collection_name=COLLECTION
    )


    return f"✅ Indexed {path.name} ({len(chunks)} chunks)"


# ---------------- SEARCH ----------------

def search_rag(query: str):

    embedder = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=BASE_URL
    )


    db = QdrantVectorStore.from_existing_collection(
        embedding=embedder,
        url=QDRANT_URL,
        collection_name=COLLECTION
    )


    docs = db.similarity_search(query, k=4)

    if not docs:
        return "❌ No relevant documents found."


    context = "\n\n".join(d.page_content for d in docs)


    llm = OllamaLLM(
        model=LLM_MODEL,
        base_url=BASE_URL
    )


    prompt = f"""
Answer using only this context.

Context:
{context}

Question:
{query}

Answer:
"""


    return llm.invoke(prompt)
