import React, { useState, useRef } from 'react';
import { UploadCloudIcon, FileTextIcon, Loader2Icon } from 'lucide-react';

export const UploadForm = ({ onAnalyze, isAnalyzing }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');
  const [jobRole, setJobRole] = useState('');
  const [useLLM, setUseLLM] = useState(true);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) { setSelectedFile(null); return; }
    if (file.type !== 'application/pdf') {
      setError('Please upload a PDF file only');
      setSelectedFile(null);
      return;
    }
    setError('');
    setSelectedFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (!file) return;
    if (file.type !== 'application/pdf') {
      setError('Please upload a PDF file only');
      return;
    }
    setError('');
    setSelectedFile(file);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedFile) { setError('Please select a file to upload'); return; }
    onAnalyze({ file: selectedFile, jobRole, useLLM });
  };

  return (
    <div className="mx-auto w-full max-w-4xl lg:max-w-5xl">
      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-lg p-6 md:p-8">
        {/* Dropzone */}
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer ${
            error ? 'border-red-400 bg-red-50' : 'border-blue-300 bg-blue-50 hover:bg-blue-100'
          } transition-colors`}
          onClick={() => fileInputRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".pdf"
            className="hidden"
          />
          {selectedFile ? (
            <div className="flex flex-col items-center">
              <FileTextIcon className="h-12 w-12 text-blue-600 mb-4" />
              <p className="text-lg font-medium text-gray-800">{selectedFile.name}</p>
              <p className="text-sm text-gray-500 mt-1">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <UploadCloudIcon className="h-12 w-12 text-blue-600 mb-4" />
              <p className="text-lg font-medium text-gray-800">Drag and drop your resume here</p>
              <p className="text-sm text-gray-500 mt-1">or click to browse (PDF only)</p>
            </div>
          )}
        </div>

        {error && <p className="mt-2 text-sm text-red-600">{error}</p>}

        {/* Options */}
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Target Job Role (optional)</label>
            <input
              type="text"
              value={jobRole}
              onChange={(e) => setJobRole(e.target.value)}
              placeholder="e.g., Software Engineer, Data Analyst"
              className="w-full rounded-lg border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <label className="flex items-center gap-2 mt-6 md:mt-auto">
            <input
              type="checkbox"
              checked={useLLM}
              onChange={(e) => setUseLLM(e.target.checked)}
              className="h-4 w-4"
            />
            <span className="text-sm text-gray-700">Use LLM for detailed feedback</span>
          </label>
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={isAnalyzing || !selectedFile}
          className={`mt-6 w-full py-3 px-4 rounded-lg font-medium text-white ${
            isAnalyzing || !selectedFile
              ? 'bg-blue-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          } transition-colors flex items-center justify-center`}
        >
          {isAnalyzing ? (
            <>
              <Loader2Icon className="animate-spin mr-2 h-5 w-5" />
              Analyzing Resume...
            </>
          ) : (
            <>Upload Resume & Analyze Now</>
          )}
        </button>

        <div className="mt-4 text-center text-sm text-gray-500">
          <p>Your resume will be analyzed for structure, content, and relevance</p>
        </div>
      </form>
    </div>
  );
};
