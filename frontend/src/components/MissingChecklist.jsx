import React from 'react';

export default function MissingChecklist({ coverage = {} }) {
  const entries = Object.entries(coverage);
  if (!entries.length) return null;

  return (
    <div className="bg-white rounded-xl border shadow-sm p-5">
      <h4 className="font-semibold text-gray-800 mb-3">Section Coverage</h4>
      <ul className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
        {entries.map(([k, ok]) => (
          <li key={k} className="flex items-center gap-2">
            <span className={ok ? 'text-green-600' : 'text-red-600'}>{ok ? '✓' : '✗'}</span>
            <span className={ok ? 'text-gray-700' : 'text-red-700'}>
              {k.charAt(0).toUpperCase() + k.slice(1)} {ok ? '' : ' — missing'}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
