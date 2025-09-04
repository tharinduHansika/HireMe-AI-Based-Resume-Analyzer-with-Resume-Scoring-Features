import React from 'react'
export const Footer = () => (
  <footer className="bg-white dark:bg-gray-800 mt-12">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="py-4 text-center text-sm text-gray-500 dark:text-gray-400">
        <p>HireMe AI Resume Analyzer — A prototype UI for resume analysis</p>
        <p className="mt-1">© {new Date().getFullYear()} HireMe. All rights reserved.</p>
      </div>
    </div>
  </footer>
)
