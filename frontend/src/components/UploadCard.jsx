import React, { useState, useRef } from 'react'
import { UploadCloudIcon, FileTextIcon } from 'lucide-react'

export const UploadCard = ({ onFileUpload, isLoading }) => {
  const [isDragging, setIsDragging] = useState(false)
  const [fileName, setFileName] = useState('')
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => { e.preventDefault(); setIsDragging(true) }
  const handleDragLeave = (e) => { e.preventDefault(); setIsDragging(false) }
  const handleDrop = (e) => {
    e.preventDefault(); setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) processFile(files[0])
  }
  const handleFileChange = (e) => { if (e.target.files.length > 0) processFile(e.target.files[0]) }
  const processFile = (file) => {
    if (file.type !== 'application/pdf') { alert('Please upload a PDF file'); return }
    setFileName(file.name)
    onFileUpload?.(file)
  }
  const handleButtonClick = () => fileInputRef.current?.click()

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
      <div className="p-6">
        <h2 className="text-lg font-medium mb-4">Upload Your Resume</h2>
        <div
          className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer ${
            isDragging ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-600'
          } ${isLoading ? 'opacity-50 pointer-events-none' : 'hover:border-blue-500 dark:hover:border-blue-400'}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleButtonClick}
        >
          <input type="file" ref={fileInputRef} onChange={handleFileChange} accept=".pdf" className="hidden" disabled={isLoading} />
          {fileName ? (
            <div className="flex items-center justify-center">
              <FileTextIcon className="h-8 w-8 text-blue-500 dark:text-blue-400" />
              <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">{fileName}</span>
            </div>
          ) : (
            <>
              <UploadCloudIcon className="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" />
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">Drag and drop your resume PDF here, or</p>
              <button type="button" className="mt-2 px-4 py-2 text-sm font-medium text-blue-700 bg-blue-100 rounded-md hover:bg-blue-200 dark:bg-blue-900 dark:text-blue-300 dark:hover:bg-blue-800" disabled={isLoading}>
                Choose PDF
              </button>
              <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">PDF files only (Max 5MB)</p>
            </>
          )}
        </div>
        {isLoading && (
          <div className="mt-4">
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
              <div className="bg-blue-600 h-2.5 rounded-full animate-pulse w-3/4"></div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-2 text-center">Analyzing your resume...</p>
          </div>
        )}
      </div>
    </div>
  )
}
