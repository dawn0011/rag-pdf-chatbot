"""FastAPI application factory with lifespan management."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import chat
from app.config import settings
from app.dependencies import preload_embeddings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for app startup and shutdown.
    Preloads the embedding model on startup to avoid cold start delay on first request.
    """
    # Startup
    print("🚀 RAG PDF Chatbot API starting...")
    
    # Create necessary directories
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    
    # Preload embedding model (approved feature)
    print("📦 Preloading embedding model...")
    preload_embeddings()
    print("✅ Embedding model loaded")
    
    yield
    
    # Shutdown
    print("🛑 RAG PDF Chatbot API shutting down...")


# Create FastAPI app with lifespan
app = FastAPI(
    title="RAG PDF Chatbot API",
    description="Upload a PDF and ask questions about it",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(chat.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "RAG PDF Chatbot API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
