# memory/store.py

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from dotenv import load_dotenv

load_dotenv()


# Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)


# Connect Qdrant
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)


def store_text(text, metadata=None):

    if metadata is None:
        metadata = {}

    vector_db.add_texts(
        texts=[text],
        metadatas=[metadata]
    )
