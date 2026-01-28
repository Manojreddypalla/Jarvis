# tools/ingest_tool.py

from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

QDRANT_URL = "http://localhost:6333"
COLLECTION = "learning_rag"

EMBED_MODEL = "mxbai-embed-large"
BASE_URL = "http://localhost:11434"


def ingest_data_folder(_=None):

    logs = []

    logs.append("📂 Scanning data folder...")

    if not DATA_DIR.exists():
        return "❌ data/ folder not found"


    files = list(DATA_DIR.glob("*"))

    if not files:
        return "ℹ️ No files found in data folder"


    logs.append(f"📁 Found {len(files)} files")


    all_chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )


    for i, file in enumerate(files, start=1):

        suffix = file.suffix.lower()

        logs.append(f"📄 [{i}/{len(files)}] Processing {file.name}")


        try:

            if suffix == ".pdf":
                loader = PyPDFLoader(str(file))

            elif suffix == ".md":
                loader = UnstructuredMarkdownLoader(str(file))

            elif suffix in [".docx", ".doc"]:
                loader = UnstructuredWordDocumentLoader(str(file))

            else:
                logs.append("⚠️ Skipped (unsupported format)")
                continue


            docs = loader.load()
            chunks = splitter.split_documents(docs)

            logs.append(f"   📦 {len(chunks)} chunks created")

            all_chunks.extend(chunks)

            file.unlink()

            logs.append("   🗑️ File deleted")


        except Exception as e:

            logs.append(f"❌ Failed: {file.name} → {e}")


    if not all_chunks:
        return "⚠️ No valid documents processed"


    logs.append("🧠 Initializing embeddings...")

    embedder = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=BASE_URL
    )


    logs.append(f"🚀 Embedding {len(all_chunks)} chunks...")


    QdrantVectorStore.from_documents(
        documents=all_chunks,
        embedding=embedder,
        url=QDRANT_URL,
        collection_name=COLLECTION
    )


    logs.append("✅ Stored in vector DB")
    logs.append("🎉 Ingestion complete!")


    return "\n".join(logs)
