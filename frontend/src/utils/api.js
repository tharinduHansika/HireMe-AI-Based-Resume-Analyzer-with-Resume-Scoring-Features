const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function analyzeResume(file, { generateLLM=false } = {}) {
  const fd = new FormData()
  fd.append('file', file)
  fd.append('generate_llm', String(generateLLM))

  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    body: fd
  })
  if (!res.ok) {
    const txt = await res.text().catch(()=> '')
    throw new Error(`Analyze failed (${res.status}): ${txt}`)
  }
  return res.json()
}
