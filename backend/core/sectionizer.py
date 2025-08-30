# core/sectionizer.py
from __future__ import annotations
import re
from typing import Dict, List, Tuple, Union

# Canonical sections with common synonyms/headers found in resumes
SECTION_SYNONYMS: Dict[str, List[str]] = {
    "summary":       [r"summary", r"profile", r"objective"],
    "experience":    [r"experience", r"employment", r"work\s+history", r"professional\s+experience"],
    "education":     [r"education", r"academics", r"qualifications"],
    "projects":      [r"projects?", r"portfolio"],
    "skills":        [r"skills?", r"technical\s+skills?", r"technologies", r"tooling"],
    "certifications":[r"certifications?", r"licenses?"],
    "contact":       [r"contact", r"contact\s+information", r"contact\s+details"],
    "links":         [r"links?", r"profiles?", r"github", r"linkedin"],
}

# The core sections we score for structure. Adjust if you like.
REQUIRED_FOR_SCORE: List[str] = ["summary", "experience", "education", "skills"]


def _find_sections_in_text(text: str) -> Dict[str, bool]:
    """Return a dict {canonical_section: True/False} by scanning headers/synonyms in the text."""
    found: Dict[str, bool] = {}
    for canon, alts in SECTION_SYNONYMS.items():
        hit = any(re.search(alt, text, flags=re.IGNORECASE | re.MULTILINE) for alt in alts)
        found[canon] = bool(hit)
    return found


def detect_section_coverage(text_or_fields: Union[str, Dict]) -> Tuple[float, Dict[str, List[str]]]:
    """
    Compute a simple structure coverage score.
    Accepts either the raw resume text (str) or the extracted fields (dict).
    Returns (score_0_to_100, details_dict)
    details = {"found": [...], "missing": [...], "flags": {section: bool}}
    """
    if isinstance(text_or_fields, str):
        flags = _find_sections_in_text(text_or_fields)
    elif isinstance(text_or_fields, dict):
        # infer presence of sections from extracted fields
        f = text_or_fields
        flags = {
            "summary":        bool(f.get("summary") or f.get("profile")),
            "experience":     bool(f.get("experience") or f.get("jobs")),
            "education":      bool(f.get("education")),
            "projects":       bool(f.get("projects")),
            "skills":         bool(f.get("skills")),
            "certifications": bool(f.get("certifications")),
            "contact":        bool(f.get("email") or f.get("phone")),
            "links":          bool(f.get("links") or f.get("profiles")),
        }
    else:
        flags = {k: False for k in SECTION_SYNONYMS}

    found_core   = [s for s in REQUIRED_FOR_SCORE if flags.get(s)]
    missing_core = [s for s in REQUIRED_FOR_SCORE if not flags.get(s)]
    score = round(100.0 * len(found_core) / max(1, len(REQUIRED_FOR_SCORE)), 1)
    return score, {"found": found_core, "missing": missing_core, "flags": flags}


# Backwards-compatibility alias (in case other code imports a different name)
section_coverage = detect_section_coverage
