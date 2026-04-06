"""Pydantic request/response schemas for API endpoints."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for the /chat endpoint."""

    question: str = Field(..., min_length=1, max_length=1000, description="User question about the PDF")


class UploadResponse(BaseModel):
    """Response body for the /upload endpoint."""

    filename: str = Field(..., description="Name of the uploaded PDF file")
    num_chunks: int = Field(..., ge=0, description="Number of text chunks created from the PDF")
    message: str = Field(..., description="Success message")


class ErrorResponse(BaseModel):
    """Generic error response."""

    detail: str = Field(..., description="Error description")
