import React from 'react';
import { RefreshCwIcon, CheckCircleIcon, AlertCircleIcon, InfoIcon } from 'lucide-react';
import { ScoreIndicator } from './ScoreIndicator';
import MissingChecklist from './MissingChecklist';
import ExtractedSummary from './ExtractedSummary';

export const ResultsDisplay = ({ results, onReset }) => {
  const { final_score, ml_score, structure_score, feedback, sectionCoverage, extracted } = results;

  const getScoreColor = (s) => (s >= 90 ? 'text-green-600' : s >= 70 ? 'text-blue-600' : s >= 50 ? 'text-yellow-600' : 'text-red-600');
  const getScoreText  = (s) => (s >= 90 ? 'Excellent' : s >= 70 ? 'Good' : s >= 50 ? 'Average' : 'Needs Improvement');

  return (
    <div className="mx-auto w-full max-w-5xl lg:max-w-6xl mt-8">
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="p-6 md:p-8 border-b">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">Resume Analysis Results</h2>
            <button onClick={onReset} className="flex items-center text-blue-600 hover:text-blue-800">
              <RefreshCwIcon className="h-4 w-4 mr-1" /> Analyze Another
            </button>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-blue-50 rounded-lg p-4 text-center">
              <h3 className="text-sm uppercase tracking-wider text-gray-500 mb-1">Final Score</h3>
              <div className="flex justify-center my-3"><ScoreIndicator score={final_score} size="lg" /></div>
              <p className={`font-bold ${getScoreColor(final_score)}`}>{getScoreText(final_score)}</p>
            </div>
            <div className="bg-blue-50 rounded-lg p-4 text-center">
              <h3 className="text-sm uppercase tracking-wider text-gray-500 mb-1">AI Score</h3>
              <div className="flex justify-center my-3"><ScoreIndicator score={ml_score} /></div>
              <p className="text-sm text-gray-600">Based on content relevance</p>
            </div>
            <div className="bg-blue-50 rounded-lg p-4 text-center">
              <h3 className="text-sm uppercase tracking-wider text-gray-500 mb-1">Structure Score</h3>
              <div className="flex justify-center my-3"><ScoreIndicator score={structure_score} /></div>
              <p className="text-sm text-gray-600">Based on resume format</p>
            </div>
          </div>
        </div>

        <div className="p-6 md:p-8">
          <h3 className="flex items-center text-lg font-medium text-gray-800 mb-4">
            <InfoIcon className="h-5 w-5 mr-2 text-blue-600" /> Feedback & Suggestions
          </h3>
          <ul className="space-y-3">
            {feedback?.map((item, index) => (
              <li key={index} className="flex items-start">
                {final_score >= 70
                  ? <CheckCircleIcon className="h-5 w-5 mr-2 text-green-500 flex-shrink-0 mt-0.5" />
                  : <AlertCircleIcon className="h-5 w-5 mr-2 text-yellow-500 flex-shrink-0 mt-0.5" />
                }
                <span className="text-gray-700">{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6 mt-6">
        <MissingChecklist coverage={sectionCoverage} />
        <ExtractedSummary extracted={extracted} />
      </div>
    </div>
  );
};
