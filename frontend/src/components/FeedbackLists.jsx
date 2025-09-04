import React from 'react'
import { ClipboardCopyIcon, DownloadIcon } from 'lucide-react'

export const FeedbackLists = ({ ruleFeedback, llmFeedback, isLoading }) => {
  const handleCopy = () => {
    const all = [
      '=== RULE-BASED FEEDBACK ===',
      ...(ruleFeedback || []),
      '',
      '=== AI-GENERATED FEEDBACK ===',
      ...(llmFeedback || []),
    ].join('\n')
    navigator.clipboard.writeText(all).then(() => alert('Feedback copied to clipboard'))
  }

  const handleDownload = () => {
    const all = [
      'RESUME ANALYSIS FEEDBACK',
      '======================',
      '',
      'RULE-BASED FEEDBACK:',
      ...(ruleFeedback || []).map(s => `- ${s}`),
      '',
      'AI-GENERATED FEEDBACK:',
      ...(llmFeedback || []).map(s => `- ${s}`),
    ].join('\n')
    const blob = new Blob([all], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = 'resume-feedback.txt'
    document.body.appendChild(a); a.click(); document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
      <div className="p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-medium">Resume Feedback</h2>
          {!isLoading && (ruleFeedback?.length || llmFeedback?.length) ? (
            <div className="flex space-x-2">
              <button onClick={handleCopy} className="inline-flex items-center px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                <ClipboardCopyIcon className="h-4 w-4 mr-1" /> Copy All
              </button>
              <button onClick={handleDownload} className="inline-flex items-center px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                <DownloadIcon className="h-4 w-4 mr-1" /> Download
              </button>
            </div>
          ) : null}
        </div>

        {isLoading ? (
          <div className="space-y-6">
            {[...Array(2)].map((_, i) => (
              <div key={i} className="space-y-2">
                <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3 animate-pulse" />
                {[...Array(3)].map((_, j) => <div key={j} className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />)}
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-6">
            <div>
              <h3 className="text-md font-medium mb-2 text-gray-800 dark:text-gray-200">Rule-Based Feedback</h3>
              {ruleFeedback?.length ? (
                <ul className="list-disc pl-5 space-y-1 text-sm text-gray-600 dark:text-gray-400">
                  {ruleFeedback.map((x, i) => <li key={i}>{x}</li>)}
                </ul>
              ) : <p className="text-sm text-gray-500 dark:text-gray-400 italic">No rule-based feedback available.</p>}
            </div>
            <div>
              <h3 className="text-md font-medium mb-2 text-gray-800 dark:text-gray-200">AI-Generated Feedback</h3>
              {llmFeedback?.length ? (
                <ul className="list-disc pl-5 space-y-1 text-sm text-gray-600 dark:text-gray-400">
                  {llmFeedback.map((x, i) => <li key={i}>{x}</li>)}
                </ul>
              ) : <p className="text-sm text-gray-500 dark:text-gray-400 italic">No AI-generated feedback available.</p>}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
