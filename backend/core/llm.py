import os
from typing import List

def _fallback_rule_based_feedback(extracted: dict, coverage: dict) -> List[str]:
    items = []

    if not coverage.get("summary"):
        items.append("Add a short professional summary at the top (2–3 lines with role, years, and key strengths).")

    if not coverage.get("skills") or len(extracted.get("skills", [])) < 8:
        items.append("Expand the skills section with 8–12 targeted, role-aligned keywords (e.g., frameworks, tools).")

    if extracted.get("experienceYears", 0) > 0:
        items.append("Quantify impact in work experience (metrics like %, time saved, revenue, users).")
    else:
        items.append("Add relevant experience entries or internships with responsibilities and technologies used.")

    if not coverage.get("certifications"):
        items.append("Include 1–2 relevant certificates (e.g., AWS CCP, Azure Fundamentals, Google Data Analytics).")

    if not coverage.get("projects") or extracted.get("projectsCount", 0) < 2:
        items.append("Show 2–3 projects with 1–2 bullet points each, focusing on tech stack and outcomes.")

    items.append("Ensure consistent formatting: headings, font sizes, and bullet alignment.")
    return items[:6]

def _build_prompt(extracted: dict, coverage: dict, scores: dict, job_role: str | None):
    role = job_role or extracted.get("jobRole") or "the target role"
    return f"""You are a precise resume reviewer. Using ONLY the facts below, create 5–7 concise, actionable bullet points of feedback tailored for {role}. Avoid generic advice. Reference missing sections explicitly. Keep each bullet under 22 words.

Extracted:
- Skills: {', '.join(extracted.get('skills', [])) or '—'}
- Experience (years): {extracted.get('experienceYears')}
- Education: {extracted.get('education') or '—'}
- Certifications: {', '.join(extracted.get('certifications', [])) or '—'}
- Projects count: {extracted.get('projectsCount')}
- Job Role (if any): {extracted.get('jobRole') or '—'}

Section coverage:
{coverage}

Scores:
Final: {scores.get('final')}, ML: {scores.get('ml')}, Structure: {scores.get('structure')}

Output strictly as a plain list of bullet sentences (no numbering, no extra commentary)."""

def generate_feedback(extracted: dict, coverage: dict, scores: dict, job_role: str | None,
                      api_key: str = "", model_name: str = "gpt-4o-mini"):
    if not api_key:
        return _fallback_rule_based_feedback(extracted, coverage)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = _build_prompt(extracted, coverage, scores, job_role)
        resp = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer. Be specific, concise, and factual."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        text = resp.choices[0].message.content.strip()
        # split into bullets safely
        lines = [l.strip("-• ").strip() for l in text.split("\n") if l.strip()]
        return [l for l in lines if l]
    except Exception:
        return _fallback_rule_based_feedback(extracted, coverage)
