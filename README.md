# RAG PDF Chatbot

A full-stack RAG (Retrieval-Augmented Generation) chatbot that lets users upload a PDF document and ask natural language questions about its content. Answers are grounded in the document and streamed in real time.

## Live Demo

- **Frontend**: [Vercel link coming soon]
- **Backend API**: [Render link coming soon]

## Project Structure

```
rag-pdf-chatbot/
├── rag-pdf-chatbot-api/       # FastAPI backend
└── rag-pdf-chatbot-frontend/  # React + Vite frontend
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite, plain JavaScript |
| Backend | FastAPI, Python |
| LLM | Groq API (llama-3.1-8b-instant) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB |
| Orchestration | LangChain v0.3 (LCEL) |
| Frontend Deploy | Vercel |
| Backend Deploy | Render |

## How It Works

1. User uploads a PDF via the frontend
2. Backend chunks and embeds the PDF into ChromaDB
3. User asks a question in the chat interface
4. Backend retrieves relevant chunks via semantic search (MMR)
5. Groq LLM generates an answer grounded in those chunks
6. Answer streams back to the frontend in real time

## Getting Started

See the individual README files for setup instructions:

- [Backend setup](rag-pdf-chatbot-api/README.md)
- [Frontend setup](rag-pdf-chatbot-frontend/README.md)

## Deployment

- Backend is deployed on Render free tier — note that cold starts may take 30-60 seconds after idle periods
- Frontend is deployed on Vercel with the `VITE_API_BASE_URL` environment variable pointing to the Render backend