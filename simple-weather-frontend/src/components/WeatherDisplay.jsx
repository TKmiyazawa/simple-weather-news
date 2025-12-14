import React from 'react'
import './WeatherDisplay.css'

// 天気アイコンのマッピング
const weatherIcons = {
  '晴れ': '☀️',
  'くもり': '☁️',
  '雨': '🌧️'
}

// 天気に応じた背景色
const weatherColors = {
  '晴れ': '#fff3e0',
  'くもり': '#eceff1',
  '雨': '#e3f2fd'
}

function WeatherDisplay({ weatherData }) {
  if (!weatherData || weatherData.length === 0) {
    return (
      <div className="weather-empty">
        <p>天気データがありません</p>
        <p>「新しいデータを生成」ボタンを押してください</p>
      </div>
    )
  }

  return (
    <div className="weather-grid">
      {weatherData.map((weather) => (
        <WeatherCard key={weather.CityId} weather={weather} />
      ))}
    </div>
  )
}

function WeatherCard({ weather }) {
  const icon = weatherIcons[weather.WeatherName] || '❓'
  const bgColor = weatherColors[weather.WeatherName] || '#ffffff'

  return (
    <div
      className="weather-card"
      style={{ backgroundColor: bgColor }}
    >
      <div className="weather-city">{weather.CityName}</div>
      <div className="weather-icon">{icon}</div>
      <div className="weather-name">{weather.WeatherName}</div>
      <div className="weather-rainfall">
        降水確率: {weather.RainfallProbability}%
      </div>
      <div className="weather-time">
        {formatTimestamp(weather.timestamp)}
      </div>
    </div>
  )
}

function formatTimestamp(timestamp) {
  if (!timestamp) return ''
  try {
    const date = new Date(timestamp)
    return date.toLocaleString('ja-JP', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return timestamp
  }
}

export default WeatherDisplay
