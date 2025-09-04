import React, { useState } from 'react'
import { UploadCard } from '../components/UploadCard'
import { TextPreview } from '../components/TextPreview'
import { SectionsGrid } from '../components/SectionsGrid'
import { FeaturesPanel } from '../components/FeaturesPanel'
import { ScoreGauge } from '../components/ScoreGauge'
import { FeedbackLists } from '../components/FeedbackLists'
import { analyzeResume } from '../utils/api'

export const AnalyzePage = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [analysisData, setAnalysisData] = useState(null)
  const [showTextPreview, setShowTextPreview] = useState(false)
  const [error, setError] = useState('')

  const handleFileUpload = async (file) => {
    try {
      setError('')
      setIsLoading(true)
      setShowTextPreview(true)
      const data = await analyzeResume(file, { generateLLM: true })
      setAnalysisData(data)
    } catch (e) {
      setError(e.message || 'Failed to analyze')
      setShowTextPreview(false)
      setAnalysisData(null)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setAnalysisData(null)
    setShowTextPreview(false)
    setError('')
  }

  const extracted = analysisData?.extractedText || ''
  const features = analysisData?.features || {}
  const sections = analysisData?.sections || {}
  const score = analysisData?.score || 0
  const modelUsed = analysisData?.modelUsed || ''
  const ruleFeedback = analysisData?.feedback?.ruleBased || []
  const llmFeedback = analysisData?.feedback?.llm || []

  return (
    <div className="w-full">
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Left Column */}
        <div className="w-full lg:w-2/5 space-y-6">
          <UploadCard onFileUpload={handleFileUpload} isLoading={isLoading} />
          {(showTextPreview || isLoading) && (
            <TextPreview text={extracted} isLoading={isLoading} />
          )}
        </div>

        {/* Right Column */}
        <div className="w-full lg:w-3/5 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 p-3 rounded">
              {error}
            </div>
          )}

          {!analysisData && !isLoading && !error && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8 text-center">
              <h2 className="text-2xl font-bold mb-4">Ready to analyze your resume</h2>
              <p className="text-gray-600 dark:text-gray-300 mb-6">
                Upload your resume PDF to get instant feedback and analysis on how well it will perform with ATS systems.
              </p>
              <div className="flex justify-center">
                <svg className="w-32 h-32 text-blue-500" viewBox="0 0 24 24" fill="none">
                  <path d="M9 17L15 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  <path d="M9 13L15 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  <path d="M9 9L15 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  <path fillRule="evenodd" clipRule="evenodd"
                    d="M3 7C3 5.34315 4.34315 4 6 4H18C19.6569 4 21 5.34315 21 7V17C21 18.6569 19.6569 20 18 20H6C4.34315 20 3 18.6569 3 17V7Z"
                    stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
            </div>
          )}

          {(analysisData || isLoading) && (
            <>
              <div className="flex justify-end">
                <button
                  onClick={handleReset}
                  className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded-md text-gray-800 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                >
                  Reset
                </button>
              </div>

              <ScoreGauge score={score} modelUsed={modelUsed} isLoading={isLoading} />
              <FeaturesPanel features={features} isLoading={isLoading} />
              <SectionsGrid sections={sections} isLoading={isLoading} />
              <FeedbackLists ruleFeedback={ruleFeedback} llmFeedback={llmFeedback} isLoading={isLoading} />
            </>
          )}
        </div>
      </div>
    </div>
  )
}
