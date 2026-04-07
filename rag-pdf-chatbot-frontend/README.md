# RAG PDF Chatbot Frontend

A React + Vite frontend for the RAG PDF Chatbot API. Upload a PDF document and ask natural language questions about its content. Answers stream in real time from the backend.

## Tech Stack

- **Framework**: React + Vite (plain JavaScript)
- **API**: Axios for uploads, Fetch + ReadableStream for streaming chat
- **Styling**: Plain CSS (Material-inspired)
- **Deployment**: Vercel

## Getting Started

### 1. Install dependencies

```bash
cd rag-pdf-chatbot-frontend
npm install
```

### 2. Configure environment

Create a `.env` file in the root of this folder:

```
VITE_API_BASE_URL=http://localhost:8000
```

For production, set this to your Render backend URL.

### 3. Run the dev server

```bash
npm run dev
```

App runs at `http://localhost:5173`

## Features

- PDF upload with progress indicator and validation (PDF only, max 10MB)
- Real-time streamed chat responses
- Friendly error messages for upload failures and API errors
- Loading states during upload and while waiting for responses

## Deployment to Vercel

1. Push code to GitHub
2. Import the repo on [Vercel](https://vercel.com)
3. Set root directory to `rag-pdf-chatbot-frontend`
4. Set environment variable: `VITE_API_BASE_URL=<your_render_backend_url>`
5. Build command: `npm run build`
6. Output directory: `dist`

## Project Structure

```
src/
├── main.jsx              # React entry point
├── App.jsx               # App state, screen switching
├── api.js                # API wrapper (upload + streaming chat)
├── styles.css            # Base styles
├── components/
│   ├── UploadScreen.jsx  # PDF upload UI
│   ├── ChatScreen.jsx    # Chat UI with streaming
│   ├── ChatMessage.jsx   # Individual message component
│   ├── Spinner.jsx       # Loading indicator
│   └── ErrorBanner.jsx   # Error display
└── utils/
    └── streamHelpers.js  # ReadableStream decoding helpers
```

## Backend

This frontend connects to the RAG PDF Chatbot API. See `rag-pdf-chatbot-api/README.md` for backend setup and endpoint documentation.