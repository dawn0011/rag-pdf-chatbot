import { useState, useRef } from 'react'
import { streamChat } from '../api'
import ChatMessage from './ChatMessage'
import Spinner from './Spinner'

export default function ChatScreen() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const abortRef = useRef(null)

  function appendMessage(msg) {
    setMessages((m) => [...m, msg])
  }

  function updateLastAssistantChunk(chunk) {
    setMessages((prev) => {
      const copy = [...prev]
      for (let i = copy.length - 1; i >= 0; i--) {
        if (copy[i].role === 'assistant') {
          copy[i] = { ...copy[i], text: (copy[i].text || '') + chunk }
          break
        }
      }
      return copy
    })
  }

  async function handleSubmit(e) {
    e?.preventDefault()
    if (!input.trim()) return

    const question = input.trim()
    // push user message
    appendMessage({ id: Date.now() + '-u', role: 'user', text: question })
    // add assistant placeholder
    appendMessage({ id: Date.now() + '-a', role: 'assistant', text: '' })

    setInput('')
    setLoading(true)

    const { abort } = streamChat(question, {
      onChunk: (chunk) => {
        updateLastAssistantChunk(chunk)
      },
      onFinish: () => {
        setLoading(false)
        abortRef.current = null
      },
      onError: (err) => {
        setLoading(false)
        const msg = err?.message || String(err)
        setError(msg)
        appendMessage({ id: Date.now() + '-err', role: 'assistant', text: 'Error: ' + msg })
        abortRef.current = null
      },
    })

    abortRef.current = abort
  }

  function handleStop() {
    if (abortRef.current) abortRef.current()
    setLoading(false)
  }

  return (
    <div style={{ maxWidth: 880, margin: '0 auto' }}>
      <div style={{ minHeight: 300, border: '1px solid #e6e9ef', borderRadius: 8, padding: 16 }}>
        {messages.length === 0 ? (
          <div style={{ color: '#6b7280' }}>No messages yet — ask something about your uploaded PDF.</div>
        ) : (
          messages.map((m) => <ChatMessage key={m.id} message={m} />)
        )}
      </div>

      {error && (
        <div style={{ marginTop: 10 }}>
          <div style={{ background: '#fee2e2', color: '#9b1c1c', padding: 10, borderRadius: 6 }}>{error}</div>
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ marginTop: 12, display: 'flex', gap: 8 }}>
        <input
          value={input}
          onChange={(e) => { setInput(e.target.value); setError(null) }}
          placeholder="Ask a question about the PDF..."
          style={{ flex: 1, padding: 10, borderRadius: 6, border: '1px solid #d1d5db' }}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()} style={{ padding: '8px 12px' }}>
          Ask
        </button>
        {loading ? (
          <button type="button" onClick={handleStop} style={{ padding: '8px 12px' }}>
            Stop
          </button>
        ) : null}
      </form>

      {loading && (
        <div style={{ marginTop: 10 }}>
          <Spinner /> <span style={{ marginLeft: 8 }}>Streaming response…</span>
        </div>
      )}
    </div>
  )
}
