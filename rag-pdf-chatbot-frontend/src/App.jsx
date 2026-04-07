import { useState } from 'react'
import UploadScreen from './components/UploadScreen'
import ChatScreen from './components/ChatScreen'
import './index.css'

function App() {
  const [uploaded, setUploaded] = useState(false)
  const [uploadedInfo, setUploadedInfo] = useState(null)

  return (
    <div id="app-root">
      {!uploaded ? (
        <UploadScreen
          onUploaded={(info) => {
            setUploaded(true)
            setUploadedInfo(info)
          }}
        />
      ) : (
        <main style={{ padding: 20 }}>
          <h2>Upload complete</h2>
          <p>{uploadedInfo?.message || `Uploaded ${uploadedInfo?.filename}`}</p>
          <p style={{ marginTop: 12 }}>
            You can now ask questions below.
          </p>
          <hr style={{ margin: '20px 0' }} />
          <ChatScreen />
        </main>
      )}
    </div>
  )
}

export default App
