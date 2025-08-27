// frontend/src/services/api.js

// Allow overriding the backend URL with an env var (Vite style).
// In development this will default to http://localhost:5000
export const API_BASE =
  import.meta?.env?.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://localhost:5000";

/**
 * POST /api/analyze
 * Expects FormData with:
 *  - file      (File)   -> the resume
 *  - job_role  (string) -> optional
 *  - use_llm   ("true"/"false")
 *
 * Returns JSON with scoring + feedback.
 */
export async function analyzeResume(formData) {
  // Do NOT set Content-Type. The browser will set the right multipart boundary.
  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  // Try to parse JSON either way so we can surface server error messages.
  let payload = null;
  try {
    payload = await res.json();
  } catch (_) {
    // ignore parse error; the response might not be JSON when backend crashes early
  }

  if (!res.ok) {
    const msg =
      (payload && (payload.error || payload.message)) ||
      `HTTP ${res.status} ${res.statusText}`;
    throw new Error(msg);
  }

  // Expect a normalized JSON object (your backend should send these fields)
  return payload;
}

/** Optional: quick health check (useful in dev) */
export async function ping() {
  try {
    const r = await fetch(`${API_BASE}/health`);
    return r.ok;
  } catch {
    return false;
  }
}
