import React, { useState, useEffect } from 'react'
import { Authenticator } from '@aws-amplify/ui-react'
import { fetchAuthSession } from 'aws-amplify/auth'
import '@aws-amplify/ui-react/styles.css'
import WeatherDisplay from './components/WeatherDisplay.jsx'
import config from './config.js'
import './App.css'

function App() {
  return (
    <Authenticator>
      {({ signOut, user }) => (
        <div className="app">
          <header className="app-header">
            <h1>天気ニュース</h1>
            <div className="user-info">
              <span>{user?.signInDetails?.loginId || 'ユーザー'}</span>
              <button onClick={signOut} className="logout-btn">
                ログアウト
              </button>
            </div>
          </header>
          <main className="app-main">
            <WeatherContent />
          </main>
          <footer className="app-footer">
            <p>サーバーレス会員制天気ニュースシステム</p>
          </footer>
        </div>
      )}
    </Authenticator>
  )
}

function WeatherContent() {
  const [weatherData, setWeatherData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchWeather = async () => {
    setLoading(true)
    setError(null)

    try {
      const session = await fetchAuthSession()
      const token = session.tokens?.idToken?.toString()

      const response = await fetch(`${config.apiEndpoint}/weather`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setWeatherData(data.data || [])
    } catch (err) {
      console.error('Weather fetch error:', err)
      setError('天気データの取得に失敗しました')
    } finally {
      setLoading(false)
    }
  }

  const generateWeather = async () => {
    setLoading(true)
    setError(null)

    try {
      const session = await fetchAuthSession()
      const token = session.tokens?.idToken?.toString()

      const response = await fetch(`${config.apiEndpoint}/weather/generate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      await fetchWeather()
    } catch (err) {
      console.error('Weather generate error:', err)
      setError('天気データの生成に失敗しました')
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchWeather()
  }, [])

  if (loading) {
    return <div className="loading">読み込み中...</div>
  }

  if (error) {
    return (
      <div className="error">
        <p>{error}</p>
        <button onClick={fetchWeather}>再試行</button>
      </div>
    )
  }

  return (
    <div className="weather-content">
      <div className="actions">
        <button onClick={fetchWeather} className="refresh-btn">
          更新
        </button>
        <button onClick={generateWeather} className="generate-btn">
          新しいデータを生成
        </button>
      </div>
      <WeatherDisplay weatherData={weatherData} />
    </div>
  )
}

export default App
