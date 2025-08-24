const API_BASE = import.meta.env.VITE_API_BASE || '';

export async function analyzeResume({ file, jobRole, useLLM }) {
  const fd = new FormData();
  fd.append('file', file);
  if (jobRole) fd.append('job_role', jobRole);
  if (useLLM) fd.append('use_llm', '1');

  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: 'POST',
    body: fd,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Analysis failed (${res.status}): ${text}`);
  }
  return res.json();
}
