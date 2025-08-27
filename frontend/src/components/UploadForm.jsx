// frontend/src/components/UploadForm.jsx
import React, { useRef, useState } from "react";
import { UploadCloudIcon, FileTextIcon, Loader2Icon, Trash2Icon } from "lucide-react";

/**
 * Props:
 * - onAnalyze(formData: FormData): Promise<void>  // parent sends to /api/analyze
 * - isAnalyzing: boolean                           // controls spinner/disabled state
 */
export default function UploadForm({ onAnalyze, isAnalyzing }) {
  const [file, setFile] = useState(null);
  const [jobRole, setJobRole] = useState("");
  const [useLLM, setUseLLM] = useState(true);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const allowedExt = ".pdf,.doc,.docx,.txt,.rtf"; // keep simple (no OCR)
  const allowedMimes = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "application/rtf",
  ];

  function validateFile(f) {
    if (!f) return "Please choose a file.";
    // If browser didn’t set MIME (sometimes happens), fall back to extension check
    const mimeOk = f.type ? allowedMimes.includes(f.type) : true;
    const extOk = allowedExt.split(",").some((ext) => f.name.toLowerCase().endsWith(ext.trim()));
    if (!mimeOk && !extOk) {
      return "Unsupported file type. Upload PDF, DOC, DOCX, TXT, or RTF.";
    }
    // 10 MB guard (optional)
    if (f.size > 10 * 1024 * 1024) {
      return "File is too large. Max 10 MB.";
    }
    return "";
  }

  const handlePick = () => fileInputRef.current?.click();

  const handleFileChange = (e) => {
    const f = e.target.files && e.target.files[0];
    const err = validateFile(f);
    setError(err);
    setFile(err ? null : f);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const f = e.dataTransfer.files && e.dataTransfer.files[0];
    const err = validateFile(f);
    setError(err);
    setFile(err ? null : f);
  };

  const clearFile = () => {
    setFile(null);
    setError("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file to analyze.");
      return;
    }
    setError("");
    try {
      const form = new FormData();
      // IMPORTANT: the key MUST be "file" for the backend
      form.append("file", file, file.name);
      form.append("job_role", jobRole || "");
      form.append("use_llm", useLLM ? "true" : "false");

      await onAnalyze(form);
    } catch (err) {
      setError(err?.message || "Upload failed.");
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-xl shadow-lg p-6 md:p-8"
      >
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${error ? "border-red-400 bg-red-50" : "border-blue-300 bg-blue-50 hover:bg-blue-100"}`}
          onClick={handlePick}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept={allowedExt}
            className="hidden"
            onChange={handleFileChange}
          />

          {file ? (
            <div className="flex flex-col items-center">
              <FileTextIcon className="h-12 w-12 text-blue-600 mb-4" />
              <p className="text-lg font-medium text-gray-800">{file.name}</p>
              <p className="text-sm text-gray-500 mt-1">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
              <button
                type="button"
                onClick={clearFile}
                className="mt-4 inline-flex items-center text-sm text-gray-600 hover:text-gray-800"
              >
                <Trash2Icon className="h-4 w-4 mr-1" /> Remove
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <UploadCloudIcon className="h-12 w-12 text-blue-600 mb-4" />
              <p className="text-lg font-medium text-gray-800">
                Drag and drop your resume here
              </p>
              <p className="text-sm text-gray-500 mt-1">
                or click to browse (PDF, DOC/DOCX, TXT, RTF)
              </p>
            </div>
          )}
        </div>

        {error && (
          <p className="mt-2 text-sm text-red-600">{error}</p>
        )}

        {/* Job role */}
        <label className="block mt-6 text-sm font-medium text-gray-700">
          Target Job Role (optional)
        </label>
        <input
          type="text"
          value={jobRole}
          onChange={(e) => setJobRole(e.target.value)}
          placeholder="e.g., Software Engineer, Data Analyst"
          className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Use LLM */}
        <div className="mt-4 flex items-center">
          <input
            id="use-llm"
            type="checkbox"
            className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
            checked={useLLM}
            onChange={(e) => setUseLLM(e.target.checked)}
          />
          <label htmlFor="use-llm" className="ml-2 text-sm text-gray-700">
            Use LLM for detailed feedback
          </label>
        </div>

        <button
          type="submit"
          disabled={isAnalyzing || !file}
          className={`mt-6 w-full py-3 px-4 rounded-lg font-medium text-white transition-colors flex items-center justify-center
            ${isAnalyzing || !file ? "bg-blue-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"}`}
        >
          {isAnalyzing ? (
            <>
              <Loader2Icon className="animate-spin mr-2 h-5 w-5" />
              Analyzing Resume...
            </>
          ) : (
            "Upload Resume & Analyze Now"
          )}
        </button>

        <div className="mt-4 text-center text-sm text-gray-500">
          Your resume will be analyzed for structure, content, and relevance.
        </div>
      </form>
    </div>
  );
}
