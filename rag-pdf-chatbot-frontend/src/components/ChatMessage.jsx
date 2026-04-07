export default function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  return (
    <div style={{
      display: 'flex',
      justifyContent: isUser ? 'flex-end' : 'flex-start',
      marginBottom: 12,
    }}>
      <div style={{
        maxWidth: '78%',
        background: isUser ? '#3b82f6' : '#f1f5f9',
        color: isUser ? 'white' : '#0f172a',
        padding: '10px 14px',
        borderRadius: 8,
        whiteSpace: 'pre-wrap',
      }}>
        {message.text}
      </div>
    </div>
  )
}
