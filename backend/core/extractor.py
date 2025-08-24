import re
from typing import Dict, List
from rapidfuzz import fuzz

SECTION_PATTERNS = {
    "skills": r"(skills|technical\s+skills|core\s+skills)\b",
    "experience": r"(experience|work\s+history|employment)\b",
    "education": r"(education|academic\s+qualifications|academic\s+background)\b",
    "certifications": r"(certification|certifications|licenses)\b",
    "projects": r"(projects|personal\s+projects)\b",
    "summary": r"(summary|professional\s+summary|objective|profile)\b",
    "contact": r"(contact|email|phone|linkedin)\b",
}

EDU_LEVELS = [
    ("phd", 4), ("doctor", 4),
    ("master", 3), ("msc", 3), ("m\.sc", 3),
    ("bachelor", 2), ("bsc", 2), ("b\.sc", 2),
    ("diploma", 1), ("higher national", 1), ("hnc", 1),
]

SKILL_SPLIT = r"[,\n;•\-\u2022]"

def _find_section_block(text: str, key_regex: str, next_headers_regex: str) -> str:
    m = re.search(key_regex, text, flags=re.I)
    if not m:
        return ""
    start = m.end()
    # find next section header after start
    nxt = re.search(next_headers_regex, text[start:], flags=re.I)
    end = start + nxt.start() if nxt else len(text)
    return text[start:end]

def _normalize_list(raw: List[str]) -> List[str]:
    clean = []
    for s in raw:
        t = re.sub(r"\s+", " ", s.strip())
        if t:
            clean.append(t)
    # dedupe with fuzzy threshold
    out = []
    for item in clean:
        if not any(fuzz.ratio(item.lower(), x.lower()) >= 92 for x in out):
            out.append(item)
    return out

def _guess_job_role(text: str) -> str | None:
    # naive guess: first occurrence of common engineering titles
    roles = ["software engineer", "software developer", "full stack", "backend developer",
             "frontend developer", "data scientist", "data analyst", "ml engineer", "devops"]
    tl = text.lower()
    for r in roles:
        if r in tl:
            return r.title()
    return None

def extract_structured_fields(text: str, fallback_job_role: str | None = None) -> Dict:
    """
    Returns keys:
      skills: List[str]
      experienceYears: float
      education: str
      certifications: List[str]
      jobRole: str | None
      projectsCount: int
    """
    if not text:
        return {
            "skills": [], "experienceYears": 0, "education": None,
            "certifications": [], "jobRole": fallback_job_role, "projectsCount": 0
        }
    headers_union = "|".join(SECTION_PATTERNS.values())
    # SKILLS
    skills_blk = _find_section_block(text, SECTION_PATTERNS["skills"], headers_union)
    raw_skills = re.split(SKILL_SPLIT, skills_blk) if skills_blk else []
    skills = _normalize_list([s for s in raw_skills if len(s.strip()) <= 40 and len(s.strip()) >= 2])

    # EXPERIENCE (years)
    years_matches = re.findall(r"(\d+\.?\d*)\s*(?:years?|yrs?)", text, flags=re.I)
    experienceYears = max([float(y) for y in years_matches], default=0.0)

    # EDUCATION (highest level text)
    edu_blk = _find_section_block(text, SECTION_PATTERNS["education"], headers_union) or text
    education = None
    for pat, _lvl in EDU_LEVELS:
        if re.search(pat, edu_blk, flags=re.I):
            # take the first matching line/phrase
            m = re.search(rf".{{0,40}}{pat}.{{0,60}}", edu_blk, flags=re.I)
            education = m.group(0).strip() if m else pat.title()
            break

    # CERTIFICATIONS
    cert_blk = _find_section_block(text, SECTION_PATTERNS["certifications"], headers_union)
    certs = _normalize_list(re.split(SKILL_SPLIT, cert_blk)) if cert_blk else []
    # naive filter to avoid noise
    certs = [c for c in certs if "cert" in c.lower() or re.search(r"\b(aws|azure|gcp|oracle|pmp|cisco)\b", c, flags=re.I)]

    # PROJECTS (count bullets/lines)
    proj_blk = _find_section_block(text, SECTION_PATTERNS["projects"], headers_union)
    projectsCount = 0
    if proj_blk:
        bullets = re.findall(r"[•\-\u2022]\s+.+", proj_blk)
        projectsCount = len(bullets) if bullets else len(re.findall(r"\bproject\b", proj_blk, flags=re.I))

    # ROLE
    jobRole = fallback_job_role or _guess_job_role(text)

    return {
        "skills": skills[:50],
        "experienceYears": experienceYears,
        "education": education,
        "certifications": certs[:20],
        "jobRole": jobRole,
        "projectsCount": int(projectsCount),
    }

def detect_section_coverage(text: str, extracted: Dict) -> Dict[str, bool]:
    cov = {}
    tl = text.lower()
    for key, pat in SECTION_PATTERNS.items():
        cov[key] = bool(re.search(pat, tl, flags=re.I))
    # reinforce with extraction results
    cov["skills"] = cov.get("skills", False) or bool(extracted.get("skills"))
    cov["experience"] = cov.get("experience", False) or extracted.get("experienceYears", 0) > 0
    cov["education"] = cov.get("education", False) or bool(extracted.get("education"))
    cov["certifications"] = cov.get("certifications", False) or bool(extracted.get("certifications"))
    cov["projects"] = cov.get("projects", False) or extracted.get("projectsCount", 0) > 0
    return cov
