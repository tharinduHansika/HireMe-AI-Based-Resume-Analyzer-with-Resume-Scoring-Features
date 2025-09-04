import React from 'react'
export const AboutPage = () => (
  <div className="max-w-3xl mx-auto">
    <h1 className="text-3xl font-bold mb-6">About HireMe AI Resume Analyzer</h1>
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
      <h2 className="text-xl font-semibold mb-4">What is HireMe?</h2>
      <p className="mb-4">
        HireMe is an AI-powered resume analyzer that helps job seekers optimize their resumes for ATS and human recruiters.
      </p>
      <p>
        It analyzes your resume against best practices and provides actionable feedback to improve your chances of landing interviews.
      </p>
    </div>
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
      <h2 className="text-xl font-semibold mb-4">How Scoring Works</h2>
      <p className="mb-4">We evaluate your resume on:</p>
      <ul className="list-disc pl-6 mb-4 space-y-2">
        <li>Content completeness (required sections)</li>
        <li>Skills relevance and presentation</li>
        <li>Experience description quality</li>
        <li>Quantifiable achievements</li>
        <li>Education details</li>
        <li>Overall readability and formatting</li>
      </ul>
      <p>Scores range from 0–100; 70+ generally indicates an ATS-friendly resume.</p>
    </div>
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Feedback System</h2>
      <p className="mb-4">We provide two types of feedback:</p>
      <div className="mb-4">
        <h3 className="font-medium mb-2">Rule-Based Feedback</h3>
        <p>Specific, actionable suggestions based on resume best practices and ATS rules.</p>
      </div>
      <div>
        <h3 className="font-medium mb-2">AI-Generated Feedback</h3>
        <p>Concise analysis that highlights strengths and improvements. No job description matching is used.</p>
      </div>
    </div>
  </div>
)
