import React from 'react';

export default function ExtractedSummary({ extracted = {} }) {
  const { skills = [], experienceYears, education, certifications = [], jobRole, projectsCount } = extracted;

  return (
    <div className="bg-white rounded-xl border shadow-sm p-5">
      <h4 className="font-semibold text-gray-800 mb-3">Extracted Summary</h4>
      <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-700">
        <div>
          <div className="font-medium">Target Job Role</div>
          <div>{jobRole || '—'}</div>
        </div>
        <div>
          <div className="font-medium">Experience (Years)</div>
          <div>{Number.isFinite(experienceYears) ? experienceYears : '—'}</div>
        </div>
        <div>
          <div className="font-medium">Education</div>
          <div>{education || '—'}</div>
        </div>
        <div>
          <div className="font-medium">Projects Count</div>
          <div>{Number.isFinite(projectsCount) ? projectsCount : '—'}</div>
        </div>
        <div className="md:col-span-2">
          <div className="font-medium">Skills</div>
          <div className="flex flex-wrap gap-2 mt-1">
            {skills.length ? skills.map((s, i) => (
              <span key={i} className="px-2 py-1 bg-blue-50 text-blue-700 rounded-md">{s}</span>
            )) : '—'}
          </div>
        </div>
        <div className="md:col-span-2">
          <div className="font-medium">Certifications</div>
          <div className="flex flex-wrap gap-2 mt-1">
            {certifications.length ? certifications.map((c, i) => (
              <span key={i} className="px-2 py-1 bg-emerald-50 text-emerald-700 rounded-md">{c}</span>
            )) : '—'}
          </div>
        </div>
      </div>
    </div>
  );
}
