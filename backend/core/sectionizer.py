# core/sectionizer.py
from __future__ import annotations
import regex as re
from typing import Dict

HEADINGS = {
    "summary":        r"(professional\s+summary|summary|profile|objective)",
    "experience":     r"(work\s+experience|professional\s+experience|experience|employment|work\s+history)",
    "education":      r"(education|academic\s+background|academics)",
    "skills":         r"(skills|areas\s+of\s+expertise|core\s+competencies|technical\s+skills|strengths)",
    "projects":       r"(projects|portfolio|selected\s+projects)",
    "certifications": r"(certifications?|licenses?|accreditations?)",
    "achievements":   r"(achievements?|awards?|accomplishments?)",
    "volunteer":      r"(volunteer|community\s+service|extracurricular)",
    "languages":      r"(languages?)",
}

COMBINED = re.compile(
    r"(?m)^(?P<h>({}))\b[^\n]*$".format("|".join([f"(?i:{p})" for p in HEADINGS.values()])),
)

def split_sections(text: str) -> Dict[str, str]:
    matches = list(COMBINED.finditer(text))
    if not matches:
        return {"_full": text}
    out: Dict[str, str] = {}
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        heading_text = m.group("h").lower()
        key = None
        for k, pat in HEADINGS.items():
            if re.search(rf"(?i)^{pat}\b", heading_text):
                key = k
                break
        if key is None:
            continue
        block = text[start:end].strip()
        if not block:
            continue
        out[key] = (out.get(key, "") + "\n\n" + block).strip()
    return out

def coverage(sections: Dict[str, str]) -> Dict[str, bool]:
    base = {k: False for k in HEADINGS.keys()}
    for k in base:
        base[k] = bool(sections.get(k))
    return base
