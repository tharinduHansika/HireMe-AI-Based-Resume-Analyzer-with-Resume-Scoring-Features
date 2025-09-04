import re
from textstat import flesch_reading_ease
from utils.dates import estimate_years_experience

NUMERIC = re.compile(r"\b\d+(?:\.\d+)?\b")
PCT     = re.compile(r"\b\d+(?:\.\d+)?\s*%")
ACHV    = re.compile(r"\b(increased|reduced|improved|boosted|cut|saved|grew|lowered|optimized)\b", re.I)

def _count_list_items(text: str) -> int:
    return len([ln for ln in (text or "").splitlines() if ln.strip().startswith(("-", "•", "·", "*"))])

def _split_skills(skills_text: str) -> list[str]:
    import re as _re
    parts = _re.split(r"[,\|;/]\s*|\n+", skills_text or "")
    return [p.strip() for p in parts if p.strip()]

def compute_features(text: str, sections: dict) -> dict:
    skills_list = _split_skills(sections.get("skills",""))
    total_words = len(re.findall(r"\b\w+\b", text or ""))
    try:
        read_score = int(max(0, min(100, flesch_reading_ease(text or ""))))
    except Exception:
        read_score = 0

    years = estimate_years_experience(sections.get("experience",""))

    quant = len(PCT.findall(text or ""))
    if quant < 3:
        quant += len([m for m in ACHV.finditer(text or "") if NUMERIC.search((text or "")[max(0,m.start()-40):m.end()+40])])

    feats = {
        "num_skills": len(skills_list),
        "has_education": bool(sections.get("education","").strip()),
        "has_experience": bool(sections.get("experience","").strip()),
        "has_contact": bool(sections.get("contact","").strip()),
        "num_projects": max(_count_list_items(sections.get("projects","")), 1 if sections.get("projects","").strip() else 0),
        "num_certifications": max(_count_list_items(sections.get("certifications","")), 1 if sections.get("certifications","").strip() else 0),
        "total_words": total_words,
        "readability_flesch": read_score,
        "years_experience_est": years,
        "quantified_achievements": quant
    }
    return feats
