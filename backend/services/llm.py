# backend/services/llm.py
import os
from openai import OpenAI

def _make_prompt(sections: dict, feats: dict, score: int) -> str:
    return f"""You are an expert technical recruiter. Analyze this resume and give concise, actionable feedback.
Output 5-8 bullet points. Avoid generic tips. Do not invent content. No job-description matching.

SCORE: {score}/100
FEATURES: {feats}

SECTIONS:
- CONTACT:
{sections.get('contact','')}
- SUMMARY:
{sections.get('summary','')}
- SKILLS:
{sections.get('skills','')}
- EXPERIENCE:
{sections.get('experience','')}
- EDUCATION:
{sections.get('education','')}
- PROJECTS:
{sections.get('projects','')}
- CERTIFICATIONS:
{sections.get('certifications','')}
- OTHER:
{sections.get('other','')}
"""

def llm_feedback_if_enabled(sections: dict, feats: dict, score: int) -> list[str]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return []

    client = OpenAI(api_key=api_key)
    prompt = _make_prompt(sections, feats, score)

    # Uses Chat Completions API (official ref). :contentReference[oaicite:4]{index=4}
    try:
        rsp = client.chat.completions.create(
            model="gpt-4o-mini",  # fast, low-cost model suitable for feedback
            messages=[
                {"role": "system", "content": "You are a precise resume reviewer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=350
        )
        text = rsp.choices[0].message.content or ""
        bullets = [ln.strip("•- \t") for ln in text.splitlines() if ln.strip()]
        return bullets[:10]
    except Exception:
        return []
