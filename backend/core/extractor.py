# core/extractor.py
import re

# very light heuristics (no OCR), designed to be robust across templates
DEGREE_KEYWORDS = [
    ("PhD", ["phd", "doctor of philosophy"]),
    ("MSc", ["msc", "master of science", "ms"]),
    ("MBA", ["mba", "master of business administration"]),
    ("BSc", ["bsc", "bachelor of science", "bs"]),
    ("BA",  ["ba", "bachelor of arts"]),
]

def _highest_degree(text: str) -> str:
    t = text.lower()
    for label, keys in DEGREE_KEYWORDS:
        for k in keys:
            if k in t:
                return label
    return ""

def _years_of_experience(text: str) -> float:
    # looks for "X years" and picks the largest X
    years = []
    for m in re.finditer(r'(\d+(?:\.\d+)?)\s*\+?\s*years?', text.lower()):
        try:
            years.append(float(m.group(1)))
        except Exception:
            pass
    return max(years) if years else 0.0

def _guess_projects_count(text: str) -> int:
    # crude: counts bullets as a proxy
    bullets = re.findall(r'[\n\r]\s*(?:[-•●◦])\s+', text)
    return min(len(bullets), 50)  # clamp

def extract_structured_fields(text: str) -> dict:
    # Skills (very rough keyword capture; you can replace with your skills_lexicon)
    maybe_skills = re.findall(r'\b([A-Za-z][A-Za-z0-9\+#\.\-]{1,})\b', text)
    # keep distinct top-N tokens that look like tech keywords
    skills = []
    seen = set()
    for tok in maybe_skills:
        if len(tok) < 2 or tok.lower() in seen:
            continue
        seen.add(tok.lower())
        skills.append(tok)
        if len(skills) >= 100:
            break

    education_highest = _highest_degree(text)
    certs = []
    for m in re.finditer(r'certifications?:?\s*(.+)', text, flags=re.IGNORECASE):
        certs.append(m.group(1).strip())
    certifications_text = "; ".join(certs)[:500]

    return {
        # for model mapping
        "skills": skills,
        "skills_text": " ".join(skills),
        "education_highest": education_highest,
        "certifications": certs,
        "certifications_text": certifications_text,
        "experience_years": _years_of_experience(text),
        "projects_count": _guess_projects_count(text),

        # for UI
        "target_role": "",
    }
