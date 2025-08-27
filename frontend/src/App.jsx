// frontend/src/App.jsx
import React, { useState } from "react";
import { Header } from "./components/Header";           // <-- named import
import { HeroSection } from "./components/HeroSection"; // <-- named import
import UploadForm from "./components/UploadForm";
import { ResultsDisplay } from "./components/ResultsDisplay";
import { analyzeResume } from "./services/api";

export default function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");

  // Receives a FormData from <UploadForm /> and calls the backend.
  const handleAnalyze = async (formData) => {
    setIsAnalyzing(true);
    setError("");
    setResults(null);

    try {
      const data = await analyzeResume(formData);

      // Defensive normalization so UI doesn't crash if a field is missing
      const normalized = {
        final_score:
          typeof data.final_score === "number"
            ? data.final_score
            : Math.round(
                ((data.ml_score ?? 0) * 0.7 + (data.structure_score ?? 0) * 0.3) || 0
              ),
        ml_score: typeof data.ml_score === "number" ? data.ml_score : 0,
        structure_score:
          typeof data.structure_score === "number" ? data.structure_score : 0,
        feedback: Array.isArray(data.feedback) ? data.feedback : [],
        // You can pass through any extra fields from backend if your ResultsDisplay uses them
        ...data,
      };

      setResults(normalized);
    } catch (e) {
      setError(e?.message || "Analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-blue-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <HeroSection />

        {/* Error banner */}
        {error && (
          <div className="mb-6 rounded-lg bg-red-50 text-red-700 px-4 py-3 text-sm">
            {error}
          </div>
        )}

        {/* Form when no results; results view otherwise */}
        {!results ? (
          <UploadForm onAnalyze={handleAnalyze} isAnalyzing={isAnalyzing} />
        ) : (
          <ResultsDisplay results={results} onReset={handleReset} />
        )}
      </main>
    </div>
  );
}
