import React from 'react'
import { CheckIcon, XIcon } from 'lucide-react'

export const FeaturesPanel = ({ features, isLoading }) => {
  const binaryFeatures = [
    { key: 'has_education', label: 'Education' },
    { key: 'has_experience', label: 'Experience' },
    { key: 'has_contact', label: 'Contact Info' },
  ]
  const numericFeatures = [
    { key: 'num_skills', label: 'Skills' },
    { key: 'num_projects', label: 'Projects' },
    { key: 'num_certifications', label: 'Certifications' },
    { key: 'years_experience_est', label: 'Years Experience' },
    { key: 'total_words', label: 'Total Words' },
    { key: 'readability_flesch', label: 'Readability Score' },
    { key: 'quantified_achievements', label: 'Quantified Achievements' },
  ]

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
      <div className="p-6">
        <h2 className="text-lg font-medium mb-4">Resume Features</h2>
        {isLoading ? (
          <div className="space-y-4">
            <div className="flex flex-wrap gap-2">
              {[...Array(3)].map((_, i) => <div key={i} className="h-8 w-24 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />)}
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              {[...Array(6)].map((_, i) => <div key={i} className="h-8 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />)}
            </div>
          </div>
        ) : (
          <>
            <div className="mb-4">
              <div className="flex flex-wrap gap-2">
                {binaryFeatures.map((f) => {
                  const value = !!features[f.key]
                  return (
                    <div key={f.key} className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${value ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'}`}>
                      {value ? <CheckIcon className="w-3 h-3 mr-1" /> : <XIcon className="w-3 h-3 mr-1" />}
                      {f.label}
                    </div>
                  )
                })}
              </div>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-x-4 gap-y-3">
              {numericFeatures.map((f) => {
                const value = features[f.key]
                const highlight = f.key === 'quantified_achievements' && value === 0
                return (
                  <div key={f.key} className={`flex justify-between ${highlight ? 'p-2 -m-2 rounded bg-yellow-50 dark:bg-yellow-900/30' : ''}`}>
                    <span className="text-sm text-gray-600 dark:text-gray-400">{f.label}:</span>
                    <span className={`text-sm font-medium ${highlight ? 'text-yellow-800 dark:text-yellow-300' : ''}`}>{value}</span>
                  </div>
                )
              })}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
