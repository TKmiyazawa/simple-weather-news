import React from 'react'
import ReactDOM from 'react-dom/client'
import { Amplify } from 'aws-amplify'
import App from './App.jsx'
import './index.css'
import config from './config.js'

// Amplify設定
Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: config.cognito.userPoolId,
      userPoolClientId: config.cognito.clientId,
    }
  }
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
