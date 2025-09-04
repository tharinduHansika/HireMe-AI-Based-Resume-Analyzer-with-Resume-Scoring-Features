import React from 'react'
export const TextPreview = ({ text, isLoading }) => (
  <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
    <div className="p-6">
      <h2 className="text-lg font-medium mb-4">Extracted Text</h2>
      <div className="relative">
        {isLoading ? (
          <div className="space-y-2">
            {[...Array(10)].map((_, i) => <div key={i} className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />)}
          </div>
        ) : (
          <div className="border border-gray-200 dark:border-gray-700 rounded-md p-4 bg-gray-50 dark:bg-gray-900 h-64 overflow-y-auto">
            <pre className="text-sm whitespace-pre-wrap text-gray-800 dark:text-gray-200 font-mono">{text}</pre>
          </div>
        )}
        <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">Bullet symbols and decorative markers removed automatically.</div>
      </div>
    </div>
  </div>
)
