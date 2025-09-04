import React, { useState } from 'react'
import { ChevronDownIcon, ChevronUpIcon, AlertCircleIcon } from 'lucide-react'

export const SectionsGrid = ({ sections, isLoading }) => {
  const [expanded, setExpanded] = useState({})
  const toggle = (key) => setExpanded(prev => ({ ...prev, [key]: !prev[key] }))

  const order = ['contact','summary','skills','experience','education','projects','certifications','other']
  const labels = {
    contact: 'Contact Information',
    summary: 'Professional Summary',
    skills: 'Skills',
    experience: 'Work Experience',
    education: 'Education',
    projects: 'Projects',
    certifications: 'Certifications',
    other: 'Additional Information'
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
      <div className="p-6">
        <h2 className="text-lg font-medium mb-4">Resume Sections</h2>
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[...Array(6)].map((_, i) => <div key={i} className="h-24 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />)}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {order.map((key) => {
              const content = sections?.[key] || ''
              const open = expanded[key]
              const isEmpty = !content?.trim()
              const isSkills = key === 'skills'
              const showWarn = isSkills && isEmpty

              return (
                <div key={key} className={`border rounded-lg ${showWarn ? 'border-yellow-300 dark:border-yellow-700 bg-yellow-50 dark:bg-yellow-900/20' : 'border-gray-200 dark:border-gray-700'}`}>
                  <div className="px-4 py-3 flex justify-between items-center cursor-pointer" onClick={() => toggle(key)}>
                    <div className="flex items-center">
                      <h3 className="font-medium">{labels[key]}</h3>
                      {showWarn && (
                        <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
                          <AlertCircleIcon className="w-3 h-3 mr-1" /> Missing
                        </span>
                      )}
                    </div>
                    {isEmpty ? (
                      <span className="text-xs text-gray-500 dark:text-gray-400">Not found</span>
                    ) : open ? (
                      <ChevronUpIcon className="h-5 w-5 text-gray-400" />
                    ) : (
                      <ChevronDownIcon className="h-5 w-5 text-gray-400" />
                    )}
                  </div>
                  {!isEmpty && open && (
                    <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700 text-sm text-gray-700 dark:text-gray-300">
                      <div className="whitespace-pre-wrap">{content}</div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
