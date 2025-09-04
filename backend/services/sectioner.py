import re
from typing import Dict, List
from utils.text_cleaning import strip_bullet_prefix

SECTION_ALIASES = {
    "contact":    [r"contact\s*information", r"contact", r"personal\s+details", r"about\s+me"],
    "summary":    [r"professional\s+summary", r"summary", r"profile", r"objective"],
    "skills":     [r"skills", r"technical\s+skills", r"core\s+competencies", r"tech\s+stack"],
    "experience": [r"experience", r"work\s+experience", r"employment", r"professional\s+experience"],
    "education":  [r"education", r"academic\s*background", r"qualifications"],
    "projects":   [r"projects?", r"personal\s+projects", r"academic\s+projects", r"selected\s+projects"],
    "certifications": [r"certifications?", r"licenses?", r"courses", r"training"],
    "other":      [r"awards", r"publications", r"languages", r"interests", r"volunteer.*", r"additional\s+information"]
}

COMPILED = {k: re.compile(rf"^\s*(?:{'|'.join(v)})\s*:?\s*$", re.I) for k, v in SECTION_ALIASES.items()}
UPPER_HEADING = re.compile(r"^[A-Z][A-Z\s/&\-]{2,40}$")
MAX_HEADING_WORDS = 8

def is_heading(line: str) -> str | None:
    l = line.strip()
    if not l: return None

    for key, rx in COMPILED.items():
        if rx.match(l):
            return key

    if UPPER_HEADING.match(l) and len(l.split()) <= MAX_HEADING_WORDS:
        lower = l.lower()
        for key, variants in SECTION_ALIASES.items():
            for v in variants:
                v0 = re.sub(r"\\s\+\?", " ", v).replace("\\s*", " ").replace("\\s+", " ")
                if v0.split()[0] in lower:
                    return key
    return None

def section_resume(text: str) -> Dict[str, str]:
    """
    Split resume into canonical sections robustly across templates.
    If a heading is not found, content stays in 'other' or inferred via heuristics.
    """
    lines = [strip_bullet_prefix(x) for x in text.splitlines()]
    current = "other"
    buckets: Dict[str, List[str]] = {k: [] for k in SECTION_ALIASES.keys()}

    contact_hint = re.compile(r"(email|@\w+|\b\d{3}[\)\-\. ]?\d{3}[\-\. ]?\d{4}\b)", re.I)

    for i, raw in enumerate(lines):
        line = raw.strip()

        sec = is_heading(line)
        if sec:
            current = sec
            continue

        if i < 10 and contact_hint.search(line) and not any(buckets["contact"]):
            buckets["contact"].append(line)
            continue

        buckets[current].append(line)

    joined = {k: "\n".join([x for x in v if x.strip()]) for k, v in buckets.items()}

    if not joined.get("summary"):
        top_block = "\n".join(lines[2:12]).strip()
        if len(top_block.split()) >= 30:
            joined["summary"] = top_block

    return joined
