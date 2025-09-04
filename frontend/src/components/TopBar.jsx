import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { SunIcon, MoonIcon } from 'lucide-react'

export const TopBar = ({ darkMode, toggleDarkMode }) => {
  const location = useLocation()
  const tab = (path) =>
    `px-3 py-2 rounded-md text-sm font-medium ${
      location.pathname === path
        ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-200'
        : 'text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700'
    }`
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center">
              <svg className="h-8 w-8 text-blue-600 dark:text-blue-400" viewBox="0 0 24 24" fill="none">
                <path d="M9 12H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                <path d="M12 9L12 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                <path fillRule="evenodd" clipRule="evenodd" d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" strokeWidth="2" />
              </svg>
              <span className="ml-2 text-xl font-bold">HireMe</span>
              <span className="ml-2 text-sm text-gray-500 dark:text-gray-400">AI Resume Analyzer</span>
            </Link>
          </div>
          <div className="flex items-center">
            <nav className="hidden md:flex space-x-4 mr-6">
              <Link to="/" className={tab('/')}>Analyze</Link>
              <Link to="/about" className={tab('/about')}>About</Link>
              <Link to="/help" className={tab('/help')}>Help</Link>
            </nav>
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-full text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {darkMode ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
