import React from 'react';

export const ScoreIndicator = ({ score, size = 'md' }) => {
  const getScoreColor = (s) => (s >= 90 ? 'text-green-600' : s >= 70 ? 'text-blue-600' : s >= 50 ? 'text-yellow-600' : 'text-red-600');
  const getTrackColor = (s) => (s >= 90 ? 'bg-green-100' : s >= 70 ? 'bg-blue-100' : s >= 50 ? 'bg-yellow-100' : 'bg-red-100');
  const getProgressColor = (s) => (s >= 90 ? 'bg-green-600' : s >= 70 ? 'bg-blue-600' : s >= 50 ? 'bg-yellow-600' : 'bg-red-600');
  const sizeClasses = { sm: 'h-2 text-xl', md: 'h-3 text-3xl', lg: 'h-4 text-4xl' };

  return (
    <div className="w-full">
      <div className="flex justify-center mb-2">
        <span className={`font-bold ${getScoreColor(score)} ${sizeClasses[size]}`}>{score}</span>
        <span className={`text-gray-500 ${size === 'lg' ? 'text-2xl' : 'text-xl'}`}>/100</span>
      </div>
      <div className={`w-full ${sizeClasses[size]} rounded-full ${getTrackColor(score)}`}>
        <div className={`${sizeClasses[size]} rounded-full ${getProgressColor(score)}`} style={{ width: `${score}%` }} />
      </div>
    </div>
  );
};
