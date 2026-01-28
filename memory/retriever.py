# memory/retriever.py

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from dotenv import load_dotenv

load_dotenv()


embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)


vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)


def search(query, k=4):

    results = vector_db.similarity_search(
        query=query,
        k=k
    )

    context = ""

    for r in results:

        text = r.page_content

        page = r.metadata.get("page", "N/A")

        context += f"""
Page: {page}
Content: {text}

----------------
"""

    return context
