"""Chat router: /upload and /chat endpoints."""

import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse

from app.config import settings
from app.models import ChatRequest, UploadResponse, ErrorResponse
from app.ingestion import ingest_pdf
from app.chain import build_rag_chain
from app.dependencies import get_vector_store, get_llm, get_retriever

# Create uploads directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    """
    Upload a PDF document for ingestion.
    Validates file extension and size.
    Clears any previous document.
    """
    # Validate file extension
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    # Validate file size (in bytes)
    max_size_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    file_content = await file.read()
    if len(file_content) > max_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit.",
        )

    if len(file_content) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # Clean up previous uploads
    if os.path.exists(settings.UPLOAD_DIR):
        shutil.rmtree(settings.UPLOAD_DIR)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Save uploaded file
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Ingest PDF
    try:
        num_chunks = await ingest_pdf(file_path)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process PDF: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during PDF processing: {str(e)}",
        )

    return UploadResponse(
        filename=file.filename,
        num_chunks=num_chunks,
        message=f"Successfully ingested {file.filename} with {num_chunks} chunks.",
    )


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Accept a question about the uploaded PDF and return a streamed answer.
    Validates that a PDF has been uploaded first.
    """
    # Validate that a PDF has been uploaded
    try:
        vector_store = get_vector_store()
        # Try to retrieve one document to check if collection has data
        results = vector_store.similarity_search(request.question, k=1)
        if not results:
            raise ValueError("No documents in collection")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No document uploaded yet. Please upload a PDF first via /upload.",
        )

    # Build the chain
    try:
        retriever = get_retriever()
        llm = get_llm()
        chain = build_rag_chain(retriever, llm)
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize RAG chain: {str(e)}",
        )

    # Stream the response
    async def generate():
        try:
            async for chunk in chain.astream(request.question):
                if chunk:
                    yield chunk
        except Exception as e:
            # Yield error message
            yield f"\n\n[Error: {str(e)}]"

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )
