import React from 'react';
import { BrainCircuitIcon } from 'lucide-react';

export const Header = () => {
  return (
    <header className="sticky top-0 bg-white shadow-sm z-10">
      <div className="container mx-auto px-4 py-4 flex items-center">
        <div className="flex items-center">
          <BrainCircuitIcon className="h-8 w-8 text-blue-600 mr-2" />
          <h1 className="text-xl font-bold text-gray-800">
            <span className="text-blue-600">HireMe</span> | AI Resume Analyzer
          </h1>
        </div>
      </div>
    </header>
  );
};
