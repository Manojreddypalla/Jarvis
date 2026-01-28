# tools/ingest_tool.py

import os
from pathlib import Path


from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore


# ---------------- CONFIG ----------------

BASE_DIR = Path(__file__).parent.parent

DATA_DIR = BASE_DIR / "data"

QDRANT_URL = "http://localhost:6333"
COLLECTION = "learning_rag"

EMBED_MODEL = "mxbai-embed-large"
BASE_URL = "http://localhost:11434"


# ---------------- MAIN TOOL ----------------

def ingest_data_folder():

    if not DATA_DIR.exists():
        return "❌ data/ folder not found"


    files = list(DATA_DIR.glob("*"))

    if not files:
        return "ℹ️ No files found in data/ folder"


    all_chunks = []


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )


    for file in files:

        suffix = file.suffix.lower()

        try:

            # -------- PDF --------
            if suffix == ".pdf":
                loader = PyPDFLoader(str(file))

            # -------- Markdown --------
            elif suffix == ".md":
                loader = UnstructuredMarkdownLoader(str(file))

            # -------- Word --------
            elif suffix in [".docx", ".doc"]:
                loader = UnstructuredWordDocumentLoader(str(file))

            else:
                continue


            docs = loader.load()

            chunks = splitter.split_documents(docs)

            all_chunks.extend(chunks)

            # Delete after successful read
            file.unlink()

            print(f"✅ Processed & deleted: {file.name}")


        except Exception as e:

            print(f"❌ Failed: {file.name} → {e}")


    if not all_chunks:
        return "⚠️ No valid documents to ingest"


    # Embeddings
    embedder = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=BASE_URL
    )


    # Store
    QdrantVectorStore.from_documents(
        documents=all_chunks,
        embedding=embedder,
        url=QDRANT_URL,
        collection_name=COLLECTION
    )


    return f"🚀 Ingested {len(all_chunks)} chunks from data folder"
