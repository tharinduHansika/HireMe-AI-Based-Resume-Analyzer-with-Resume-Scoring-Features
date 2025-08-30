# backend/core/validator.py
import re
from typing import Dict, List, Tuple
from .skills_lexicon import SKILL_WORDS, SKILL_PHRASES, CANONICAL, BANNED_TOKENS

EMAIL_RE   = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
URL_RE     = re.compile(r"https?://\S+|www\.\S+")
YEARS_RE   = re.compile(r"(\d+)\s*\+?\s*(?:years?|yrs)\b", re.I)
RANGE_RE   = re.compile(r"(\d{4})\s*[-–]\s*(\d{4}|present|current)", re.I)
DEGREE_RE  = re.compile(r"\b(BSc|BS|MSc|MS|BA|MA|MBA|B\.?Eng|M\.?Eng|PhD)\b", re.I)
EDU_HINTS  = re.compile(r"\b(university|college|institute|academy|school)\b", re.I)
CERT_RE    = re.compile(r"\b(certified|certificate|certification|qualification|license|licensed)\b", re.I)
PROJECT_RE = re.compile(r"\bprojects?\b", re.I)

def _norm_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def _canonical_skill(tok: str) -> str:
    t = tok.lower().strip()
    t = t.replace("-", "-")  # fix non-standard hyphen
    if t in CANONICAL:
        return CANONICAL[t]
    # Title-case most words, but preserve obvious ALLCAPS acronyms
    if t.isupper():
        return t
    if t in {"html", "css", "sql", "ux", "ui"}:
        return CANONICAL.get(t, t.upper())
    return t.replace("-", " ").title()

def _find_phrases(text_lc: str) -> List[str]:
    found = []
    for p in SKILL_PHRASES:
        if p in text_lc:
            found.append(_canonical_skill(p))
    return found

def _find_words(text_lc: str) -> List[str]:
    # conservative tokenization
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9\.\+\#\-]*", text_lc)
    out = []
    for t in tokens:
        t_lc = t.lower()
        if t_lc in SKILL_WORDS and t_lc not in BANNED_TOKENS:
            out.append(_canonical_skill(t_lc))
    return out

def _dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out  = []
    for x in items:
        if not x:
            continue
        if x.lower() in seen:
            continue
        seen.add(x.lower())
        out.append(x)
    return out

def _extract_education_lines(text: str) -> List[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    edu = []
    for ln in lines:
        if DEGREE_RE.search(ln) or EDU_HINTS.search(ln):
            # strip email/urls
            ln2 = EMAIL_RE.sub("", ln)
            ln2 = URL_RE.sub("", ln2)
            ln2 = _norm_ws(ln2)
            if len(ln2) > 3:
                edu.append(ln2)
    # keep top 3 distinct lines
    return _dedupe_keep_order(edu)[:3]

def _extract_certifications(text: str) -> List[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    out = []
    for ln in lines:
        if CERT_RE.search(ln):
            ln2 = URL_RE.sub("", EMAIL_RE.sub("", ln))
            ln2 = _norm_ws(ln2)
            if len(ln2) > 3:
                out.append(ln2)
    return _dedupe_keep_order(out)[:5]

def _years_of_experience(text: str) -> float:
    # 1) explicit "X years" mentions
    m = YEARS_RE.search(text)
    if m:
        try:
            return float(m.group(1))
        except:
            pass
    # 2) sum of year ranges like "2019-2023", "2021 - Present"
    total = 0.0
    for y1, y2 in RANGE_RE.findall(text):
        try:
            start = int(y1)
            end = (int(y2) if y2.isdigit() else 2025)  # crude: treat present/current as this year
            if end >= start and 0 < (end - start) < 50:
                total += (end - start)
        except:
            continue
    if total > 0:
        return round(total, 1)
    return 0.0

def _projects_count(text: str) -> int:
    # approximate: counts bullets/mentions near word "project"
    lines = [l.strip().lower() for l in text.splitlines() if l.strip()]
    count = 0
    for ln in lines:
        if "project" in ln:
            # heuristic: bullet or numeric list indicates an item
            if ln.startswith(("-", "•", "*")) or re.match(r"^\d+[\).\-\s]", ln):
                count += 1
    if count == 0:
        # fallback: occurrences of the word
        count = len(PROJECT_RE.findall(text))
        if count > 6:  # clamp noisy counts
            count = 6
    return int(count)

def normalize_fields_for_ui(raw: Dict, text: str, job_role: str = "") -> Dict:
    """
    Accepts raw dict from extract_structured_fields(...) and raw text.
    Returns the normalized object the UI expects.
    """
    text_lc = text.lower()

    # SKILLS = phrases + single words, cleaned
    skills = _find_phrases(text_lc) + _find_words(text_lc)
    skills = [s for s in skills if s.lower() not in BANNED_TOKENS]
    skills = _dedupe_keep_order(skills)[:40]

    edu = raw.get("education") or _extract_education_lines(text)
    edu = _dedupe_keep_order([_norm_ws(x) for x in edu])[:3]

    certs = raw.get("certifications") or _extract_certifications(text)
    certs = _dedupe_keep_order([_norm_ws(x) for x in certs])[:6]

    exp_years = raw.get("experience_years")
    if exp_years is None:
        exp_years = _years_of_experience(text)

    proj_count = raw.get("projects_count")
    if proj_count is None:
        proj_count = _projects_count(text)

    return {
        "target_job_role": (job_role or raw.get("job_role") or "").strip(),
        "experience_years": float(exp_years or 0.0),
        "projects_count": int(proj_count or 0),
        "education": edu,
        "skills": skills,
        "certifications": certs,
    }
