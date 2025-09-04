import React from 'react'
export const ScoreGauge = ({ score, modelUsed, isLoading }) => {
  const color = (s) => (s >= 80 ? 'text-green-500' : s >= 60 ? 'text-blue-500' : s >= 40 ? 'text-yellow-500' : 'text-red-500')
  const scoreColor = color(score)
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
      <div className="p-6">
        <h2 className="text-lg font-medium mb-4">Resume Score</h2>
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-4">
            <div className="w-32 h-32 rounded-full border-8 border-gray-200 dark:border-gray-700 animate-pulse"></div>
            <div className="mt-4 h-6 bg-gray-200 dark:bg-gray-700 rounded w-24 animate-pulse"></div>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <div className="relative">
              <svg className="w-32 h-32" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="none" stroke="#e5e7eb" strokeWidth="10" className="dark:stroke-gray-700" />
                <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" strokeWidth="10" strokeDasharray={`${score * 2.83} 283`} strokeLinecap="round" transform="rotate(-90 50 50)" className={scoreColor} />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center flex-col">
                <span className={`text-3xl font-bold ${scoreColor}`}>{score}</span>
                <span className="text-sm text-gray-500 dark:text-gray-400">/ 100</span>
              </div>
            </div>
            <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">Model: {modelUsed || 'AI Resume Analyzer v1.0'}</div>
            {score < 45 && (
              <div className="mt-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
                Improve readability
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
