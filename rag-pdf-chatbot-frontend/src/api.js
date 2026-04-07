const API_BASE = import.meta.env.VITE_API_BASE_URL;

import axios from 'axios';

export async function uploadPdf(file, onProgress) {
  if (!file) throw new Error('No file provided');
  const form = new FormData();
  form.append('file', file, file.name);

  try {
    const resp = await axios.post(`${API_BASE}/api/upload`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.lengthComputable) {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percent);
        }
      },
    });
    return resp.data;
  } catch (err) {
    // Normalize error messages from axios
    if (err.response) {
      const status = err.response.status
      const data = err.response.data
      const serverMessage = data && (data.message || data.error || data.detail)
      if (status === 413) throw new Error('File is too large (max 10MB).')
      if (status === 400 && serverMessage) throw new Error(serverMessage)
      throw new Error(serverMessage || `Upload failed with status ${status}`)
    }
    throw new Error(err.message || 'Network error during upload')
  }
}

// streamChat: sends a question and streams plain-text chunks from the backend
// onChunk(chunkText) called for each incoming text chunk
// returns an object with `abort()` to cancel the request
export function streamChat(question, { onChunk, onFinish, onError } = {}) {
  const controller = new AbortController();

  (async () => {
    try {
      const resp = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
        signal: controller.signal,
      });

      if (!resp.ok) {
        // try to parse json error message
        const ct = resp.headers.get('content-type') || ''
        let text = ''
        try {
          if (ct.includes('application/json')) {
            const obj = await resp.json()
            text = obj?.message || obj?.error || JSON.stringify(obj)
          } else {
            text = await resp.text()
          }
        } catch {
          text = `Request failed with status ${resp.status}`
        }
        throw new Error(text || `Request failed with status ${resp.status}`)
      }

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          if (onChunk) onChunk(chunk);
        }
      }

      if (onFinish) onFinish();
    } catch (err) {
      if (err.name === 'AbortError') {
        // aborted by caller; treat as finished
        if (onFinish) onFinish();
      } else {
        if (onError) onError(err);
      }
    }
  })();

  return { abort: () => controller.abort() };
}

export default { uploadPdf, streamChat };
