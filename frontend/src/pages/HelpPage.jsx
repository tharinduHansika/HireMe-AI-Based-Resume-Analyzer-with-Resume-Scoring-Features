import React from 'react'
export const HelpPage = () => (
  <div className="max-w-3xl mx-auto">
    <h1 className="text-3xl font-bold mb-6">Help & FAQ</h1>
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
      <h2 className="text-xl font-semibold mb-4">Frequently Asked Questions</h2>
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-medium mb-2">What file formats are supported?</h3>
          <p>PDF only. Use a text-based PDF (not an image scan).</p>
        </div>
        <div>
          <h3 className="text-lg font-medium mb-2">How accurate is the analysis?</h3>
          <p>It combines rule-based checks and ML features (readability, achievements, section completeness) for robust scoring.</p>
        </div>
        <div>
          <h3 className="text-lg font-medium mb-2">What sections are analyzed?</h3>
          <ul className="list-disc pl-6 space-y-1">
            <li><strong>Contact</strong></li>
            <li><strong>Summary</strong></li>
            <li><strong>Skills</strong></li>
            <li><strong>Experience</strong></li>
            <li><strong>Education</strong></li>
            <li><strong>Projects</strong></li>
            <li><strong>Certifications</strong></li>
            <li><strong>Other</strong></li>
          </ul>
        </div>
        <div>
          <h3 className="text-lg font-medium mb-2">Is my data secure?</h3>
          <p>In this prototype, the file is processed only by your local backend and not stored.</p>
        </div>
      </div>
    </div>
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Understanding Your Score</h2>
      <ul className="list-disc pl-6 space-y-2">
        <li><strong>70–100:</strong> Excellent (ATS-friendly)</li>
        <li><strong>50–69:</strong> Good (some improvements)</li>
        <li><strong>30–49:</strong> Fair (needs multiple improvements)</li>
        <li><strong>0–29:</strong> Needs work (likely ATS-filtered)</li>
      </ul>
    </div>
  </div>
)
