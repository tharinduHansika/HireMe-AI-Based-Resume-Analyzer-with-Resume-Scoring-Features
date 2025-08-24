import React, { useState } from 'react';
import { Header } from './components/Header';
import { HeroSection } from './components/HeroSection';
import { UploadForm } from './components/UploadForm';
import { ResultsDisplay } from './components/ResultsDisplay';
import { analyzeResume } from './services/api';

export function App() {
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async ({ file, jobRole, useLLM }) => {
    setIsAnalyzing(true);
    setError('');
    try {
      const data = await analyzeResume({ file, jobRole, useLLM });
      const normalized = {
        final_score: data?.scores?.final ?? 0,
        ml_score: data?.scores?.ml ?? 0,
        structure_score: data?.scores?.structure ?? 0,
        feedback: data?.llmFeedback ?? [],
        sectionCoverage: data?.sectionCoverage ?? {},
        extracted: data?.extracted ?? {},
        featureVector: data?.featureVector ?? {},
      };
      setAnalysisResults(normalized);
    } catch (e) {
      console.error(e);
      setError(e.message || 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-blue-50">
      <Header />
      <main className="max-w-screen-2xl mx-auto px-4 py-8">
        <HeroSection />
        {error && (
          <div className="max-w-3xl mx-auto mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {error}
          </div>
        )}
        {!analysisResults && (
          <UploadForm onAnalyze={handleAnalyze} isAnalyzing={isAnalyzing} />
        )}
        {analysisResults && (
          <ResultsDisplay
            results={analysisResults}
            onReset={() => setAnalysisResults(null)}
          />
        )}
      </main>
    </div>
  );
}
