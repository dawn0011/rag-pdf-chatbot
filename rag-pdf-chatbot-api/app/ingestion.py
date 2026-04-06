"""PDF ingestion pipeline: load, split, embed, and store in ChromaDB."""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.dependencies import get_vector_store


async def ingest_pdf(file_path: str) -> int:
    """
    Load a PDF, validate it, chunk it, and embed it into ChromaDB.
    Clears the existing collection before adding new documents (single-doc model).

    Args:
        file_path: Path to the PDF file

    Returns:
        Number of chunks created

    Raises:
        ValueError: If PDF is empty or has no text content
        FileNotFoundError: If file does not exist
    """
    # Check file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    # Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Validate: has pages
    if not docs:
        raise ValueError("PDF has no pages or could not be read")

    # Validate: has text content
    total_text = "".join(doc.page_content for doc in docs).strip()
    if not total_text:
        raise ValueError("PDF has no extractable text content")

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        add_start_index=True,
    )
    splits = text_splitter.split_documents(docs)

    if not splits:
        raise ValueError("PDF could not be split into chunks")

    # Get vector store and clear existing collection (single-doc model)
    vector_store = get_vector_store()
    
    # Delete existing collection to replace it
    try:
        client = vector_store._client
        client.delete_collection(name=settings.CHROMA_COLLECTION)
    except Exception:
        # Collection may not exist yet, that's fine
        pass
    
    # Reset the global singleton so next request gets a fresh instance
    import app.dependencies
    app.dependencies._vector_store = None
    
    # Get a fresh vector store instance
    vector_store = get_vector_store()

    # Add documents to vector store
    vector_store.add_documents(splits)

    return len(splits)
