import React, { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import { AnalyzePage } from './pages/AnalyzePage'
import { AboutPage } from './pages/AboutPage'
import { HelpPage } from './pages/HelpPage'
import { TopBar } from './components/TopBar'
import { Footer } from './components/Footer'

export function App() {
  const [darkMode, setDarkMode] = useState(false)
  const toggleDarkMode = () => setDarkMode(v => !v)

  return (
    <div className={`min-h-screen flex flex-col ${darkMode ? 'dark bg-gray-900 text-white' : 'bg-white text-gray-900'}`}>
      <TopBar darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      <main className="flex-grow w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Routes>
          <Route path="/" element={<AnalyzePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/help" element={<HelpPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}
