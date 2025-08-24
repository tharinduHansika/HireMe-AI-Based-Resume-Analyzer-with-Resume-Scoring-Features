import React from 'react';
import { FileTextIcon, SparklesIcon } from 'lucide-react';

export const HeroSection = () => {
  return (
    <section className="py-12 md:py-20 text-center">
      <div className="mx-auto max-w-5xl md:max-w-6xl 2xl:max-w-7xl">
        <div className="mb-6 flex justify-center">
          <div className="relative">
            <FileTextIcon className="h-16 w-16 text-blue-600" />
            <SparklesIcon className="h-8 w-8 text-yellow-500 absolute -top-2 -right-2 animate-pulse" />
          </div>
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          AI-Powered Resume Analyzer
        </h1>
        <p className="text-xl md:text-2xl text-gray-600 mb-8">
          Upload your resume. Get instant feedback. Land your dream job.
        </p>
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          <div className="flex items-center bg-blue-50 p-3 rounded-lg">
            <div className="bg-blue-100 rounded-full p-2 mr-3">
              <SparklesIcon className="h-5 w-5 text-blue-600" />
            </div>
            <p className="text-gray-700">AI-powered analysis</p>
          </div>
          <div className="flex items-center bg-blue-50 p-3 rounded-lg">
            <div className="bg-blue-100 rounded-full p-2 mr-3">
              <FileTextIcon className="h-5 w-5 text-blue-600" />
            </div>
            <p className="text-gray-700">Detailed feedback</p>
          </div>
        </div>
      </div>
    </section>
  );
};
