"""
Singleton dependency providers for embeddings, vector store, and LLM.
Implements lazy loading with optional preloading during app startup.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.retrievers import BaseRetriever

from app.config import settings

# Module-level singletons (lazily initialized)
_embeddings: HuggingFaceEmbeddings | None = None
_vector_store: Chroma | None = None
_llm: ChatGroq | None = None


def get_embeddings() -> HuggingFaceEmbeddings:
    """Get or create the embeddings model (lazy-loaded)."""
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
    return _embeddings


def get_vector_store() -> Chroma:
    """Get or create the ChromaDB vector store (lazy-loaded)."""
    global _vector_store
    if _vector_store is None:
        embeddings = get_embeddings()
        _vector_store = Chroma(
            collection_name=settings.CHROMA_COLLECTION,
            embedding_function=embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIR,
        )
    return _vector_store


def get_llm() -> ChatGroq:
    """Get or create the Groq LLM (lazy-loaded)."""
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0.2,
            streaming=True,
        )
    return _llm


def get_retriever() -> BaseRetriever:
    """Get a retriever from the vector store."""
    vector_store = get_vector_store()
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": settings.RETRIEVER_K, "fetch_k": settings.RETRIEVER_K * 2},
    )


def preload_embeddings() -> None:
    """
    Preload the embedding model during app startup.
    Shifts the model loading time from first request to deployment time.
    """
    get_embeddings()
