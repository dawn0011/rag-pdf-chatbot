export default function ErrorBanner({ message }) {
  if (!message) return null
  return (
    <div style={{
      background: '#ffe7e7',
      color: '#800',
      padding: 12,
      borderRadius: 6,
      marginBottom: 8,
    }}>{message}</div>
  )
}
