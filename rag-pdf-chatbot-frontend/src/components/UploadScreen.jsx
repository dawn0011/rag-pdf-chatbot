import { useState } from 'react'
import { uploadPdf } from '../api'
import Spinner from './Spinner'
import ErrorBanner from './ErrorBanner'

export default function UploadScreen({ onUploaded }) {
  const [file, setFile] = useState(null)
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const MAX_MB = 10

  function handleFile(e) {
    setError(null)
    const f = e.target.files[0]
    setFile(f)
  }

  async function handleUpload() {
    setError(null)
    if (!file) return setError('Please select a PDF file to upload.')
    if (file.type !== 'application/pdf') return setError('Only PDF files are allowed.')
    if (file.size > MAX_MB * 1024 * 1024) return setError(`File must be <= ${MAX_MB}MB.`)

    setLoading(true)
    setProgress(0)
    try {
      const resp = await uploadPdf(file, (p) => setProgress(p))
      setLoading(false)
      setProgress(100)
      if (onUploaded) onUploaded(resp)
    } catch (err) {
      setLoading(false)
      // Provide friendly mapped messages where possible
      const msg = err?.message || 'Upload failed'
      setError(msg)
    }
  }

  return (
    <div style={{ maxWidth: 720, margin: '40px auto', padding: 20 }}>
      <h1>Upload PDF</h1>
      <p>Select a PDF (max 10MB) to ingest into the backend.</p>

      {error && <ErrorBanner message={error} />}

      <div style={{ marginTop: 12 }}>
        <input type="file" accept="application/pdf" onChange={handleFile} />
      </div>

      <div style={{ marginTop: 16 }}>
        <button onClick={handleUpload} disabled={loading}>
          {loading ? 'Uploading…' : 'Upload PDF'}
        </button>
      </div>

      {loading && (
        <div style={{ marginTop: 12 }}>
          <Spinner />
          <div style={{ marginTop: 8 }}>Progress: {progress}%</div>
        </div>
      )}
    </div>
  )
}
