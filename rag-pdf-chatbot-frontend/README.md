# RAG PDF Chatbot Frontend

A modern React + Vite frontend for a Retrieval-Augmented Generation (RAG) PDF chatbot. Upload a PDF document and ask natural language questions — answers stream in real time from the backend.

---

## 🚀 Tech Stack

* **Framework**: React + Vite (JavaScript)
* **HTTP Client**: Axios (file uploads)
* **Streaming**: Fetch API + ReadableStream
* **Styling**: Plain CSS (Material-inspired)
* **Deployment**: Vercel

---

## 📦 Getting Started

### 1. Install dependencies

```bash
npm install
```

---

### 2. Configure environment

Create a `.env.development` file in the project root:

```env
VITE_API_BASE_URL=http://localhost:8000
```

For production, set the environment variable in your deployment platform:

```env
VITE_API_BASE_URL=https://your-backend-domain.com
```

> ⚠️ Note:
> This project does **not use Vite proxy**. All API requests are made directly using `VITE_API_BASE_URL`.

---

### 3. Run the development server

```bash
npm run dev
```

App runs at:

```
http://localhost:5173
```

---

## ✨ Features

* 📄 PDF upload with progress tracking
* ⚡ Real-time streaming chat responses
* ❌ Friendly error handling (upload + API errors)
* ⏳ Loading states for better UX
* 🔒 File validation (PDF only, max 10MB)

---

## 🏗️ Project Structure

```
src/
├── main.jsx              # React entry point
├── App.jsx               # App state and routing
├── api.js                # API wrapper (upload + streaming chat)
├── styles.css            # Global styles
├── components/
│   ├── UploadScreen.jsx  # PDF upload UI
│   ├── ChatScreen.jsx    # Chat UI with streaming
│   ├── ChatMessage.jsx   # Chat message component
│   ├── Spinner.jsx       # Loading indicator
│   └── ErrorBanner.jsx   # Error display
└── utils/
    └── streamHelpers.js  # Stream decoding helpers
```

---

## 🔗 Backend

This frontend connects to the RAG PDF Chatbot API.

Make sure your backend:

* is running and accessible
* allows CORS from your frontend domain
* exposes:

  * `POST /api/upload`
  * `POST /api/chat` (streaming)

Refer to your backend repository for setup details.

---

## ⚠️ Environment Variables

* Only variables prefixed with `VITE_` are exposed to the frontend
* Do **not** store secrets in these variables

Example:

```env
VITE_API_BASE_URL=https://api.example.com
```

---

## 📄 License

This project is for educational and demonstration purposes.
