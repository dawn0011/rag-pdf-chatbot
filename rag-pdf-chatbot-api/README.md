# RAG PDF Chatbot API

A FastAPI backend for a Retrieval-Augmented Generation (RAG) chatbot that lets users upload PDF documents and ask natural language questions about their content. Answers are streamed and grounded in the document using LangChain, ChromaDB, HuggingFace embeddings, and Groq's LLM.

## Features

- 📄 **PDF Upload** — user-friendly document ingestion with validation
- 🔍 **Semantic Search** — retrieve relevant chunks using MMR (Maximal Marginal Relevance)
- 💬 **Streamed Q&A** — real-time answers from Groq's Llama 3.1 model via LCEL chains
- 🗄️ **Persistent Storage** — ChromaDB stores embeddings locally
- ⚡ **Model Preloading** — embedding model loads at startup to avoid cold start delays
- 🔒 **Error Handling** — graceful handling of empty PDFs, API failures, and invalid inputs

## Tech Stack

- **Framework**: FastAPI
- **LLM**: Groq API (llama-3.1-8b-instant)
- **Embeddings**: HuggingFace (sentence-transformers/all-MiniLM-L6-v2)
- **Vector Store**: ChromaDB (persistent local storage)
- **Orchestration**: LangChain v0.3 with LCEL pipe syntax
- **Deployment**: Render free tier (no external dependencies)

## Setup

### 1. Clone and Install

```bash
git clone <repo>
cd rag-pdf-chatbot-api
uv sync
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your Groq API key:

```bash
cp .env.example .env
# Edit .env and set GROQ_API_KEY=<your_key>
```

Get a free API key from [Groq Console](https://console.groq.com).

### 3. Run the Server

```bash
python main.py
```

Server starts on `http://localhost:8000`

Check health: `http://localhost:8000/health`

## API Endpoints

### Upload a PDF

**`POST /api/upload`**

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "filename": "document.pdf",
  "num_chunks": 42,
  "message": "Successfully ingested document.pdf with 42 chunks."
}
```

**Error cases:**
- Non-PDF file → 400 Bad Request
- File > 10MB → 413 Payload Too Large
- Empty file → 400 Bad Request
- Unparseable PDF → 400 Bad Request

### Ask a Question

**`POST /api/chat`**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

**Response:** Streamed plain text answer (chunked)

**Error cases:**
- No PDF uploaded yet → 400 Bad Request
- Groq API failure → 500 Internal Server Error

## Configuration

Edit `app/config.py` or set environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `GROQ_API_KEY` | (required) | Groq API authentication |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | LLM model to use |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |
| `CHUNK_SIZE` | `1000` | Text chunk size (chars) |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `RETRIEVER_K` | `4` | Number of chunks to retrieve |
| `MAX_UPLOAD_SIZE_MB` | `10` | Max PDF file size |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | ChromaDB storage location |

## Architecture

```
main.py (FastAPI app, lifespan, CORS)
├── app/
│   ├── config.py (Settings from .env)
│   ├── models.py (Pydantic schemas)
│   ├── dependencies.py (Lazy-loaded singletons: embeddings, vector store, LLM)
│   ├── ingestion.py (PDF load → split → embed → ChromaDB)
│   ├── chain.py (LCEL RAG pipeline)
│   └── routers/
│       └── chat.py (POST /upload, POST /chat)
├── chroma_db/ (Persistent embeddings)
├── uploads/ (Temp PDF storage)
└── pyproject.toml (Dependencies)
```

## How It Works

1. **Upload** → PDF loaded with PyPDFLoader, split into overlapping chunks, embedded with HuggingFace embeddings, stored in ChromaDB
2. **Chat** → Question is embedded, MMR search retrieves top-k chunks, chunks + question fed to prompt template, Groq LLM streams response, streamed back to client
3. **Single Document** → New upload clears the previous collection (no multi-doc sessions)

## Deployment to Render

1. Push code to GitHub
2. Create new Web Service on [Render](https://render.com)
3. Connect GitHub repo
4. Set environment variable: `GROQ_API_KEY=<your_key>`
5. Render auto-detects `pyproject.toml` and builds/deploys
6. Service restarts periodically (Render free tier) — ChromaDB data is ephemeral

**Note:** On Render's free tier (~512MB RAM), the embedding model (`all-MiniLM-L6-v2` at ~80MB) preloads at startup. Cold starts may take 30–60 seconds after idle periods.

## Development

### Run with live reload

```bash
python main.py
```

### Test endpoints

```bash
# Health check
curl http://localhost:8000/health

# Upload a test PDF
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test.pdf"

# Ask a question
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

## Limitations & Known Issues

- **Single Document**: Only one PDF at a time (new upload clears the previous one)
- **Ephemeral Storage**: On Render, embeddings are lost on redeploy or restart
- **No Authentication**: No user sessions or API keys
- **Streaming Format**: Plain text streaming (UTF-8) — clients must parse chunks

## Future Enhancements

- Multi-document support with collection management
- Session persistence (Redis)
- User authentication (API keys, OAuth)
- Document metadata (title, upload date)
- Query history
- Configurable LLM models/parameters
- Web UI (frontend)

## License

MIT

## Support

For issues or questions, open a GitHub issue.
