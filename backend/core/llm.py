# core/llm.py
from __future__ import annotations
import os

def generate_feedback(
    extracted: dict,
    coverage: dict,
    scores: dict,
    job_role: str | None,
    api_key: str | None,
    model_name: str = "gpt-4o-mini",
):
    # Rule-based fallback
    if not api_key:
        tips = []
        if not coverage.get("summary"): tips.append("Add a 2–3 sentence Professional Summary aligned to your target role.")
        if len(extracted.get("skills", [])) < 8: tips.append("Expand Skills with 8–15 role-specific keywords from the job description.")
        if not coverage.get("certifications"): tips.append("List relevant certifications (e.g., AWS, Scrum) if you have them.")
        if (extracted.get("experienceYears") or 0) > 0: tips.append("Quantify achievements with metrics (%, $, time saved, scale).")
        if not coverage.get("projects"): tips.append("Add 2–3 Projects with problem, action, measurable results.")
        if scores.get("structure", 100) < 80: tips.append("Improve formatting: clear headers, consistent bullets, and spacing.")
        return tips

    # LLM path
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        target = job_role or extracted.get("jobRole") or "Not specified"
        skills = ", ".join(extracted.get("skills", [])[:20]) or "None detected"
        yrs = extracted.get("experienceYears") or 0
        edu = extracted.get("education") or "Not detected"
        certs = ", ".join(extracted.get("certifications", [])[:10]) or "None"
        projects = extracted.get("projectsCount") or 0

        prompt = f"""
You are an expert resume reviewer and ATS coach.
Target role: {target}

Extracted snapshot:
- Skills: {skills}
- Experience (years): {yrs}
- Education: {edu}
- Certifications: {certs}
- Projects count: {projects}
- Section coverage: {coverage}
- Scores: {scores}

Write at most 8 crisp, actionable suggestions to improve this resume for ATS and recruiters.
Rules:
- Be specific and role-aware.
- Use imperative voice ("Do X"), add concrete examples.
- Emphasize quantification, relevant keywords, and formatting.
- If a section is missing, call it out explicitly.
Output as bullet list, each bullet under ~25 words.
"""
        resp = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        text = resp.choices[0].message.content.strip()
        bullets = [ln.strip(" -•") for ln in text.splitlines() if ln.strip()]
        return bullets[:8]
    except Exception:
        return ["Enable LLM for tailored guidance. Meanwhile: add summary, expand skills with JD keywords, quantify results, and ensure clear, consistent formatting."]
