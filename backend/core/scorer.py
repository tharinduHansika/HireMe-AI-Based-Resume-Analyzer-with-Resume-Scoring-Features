# backend/core/scorer.py
from __future__ import annotations
from typing import Dict, Any

# Sections we expect in a resume
EXPECTED_SECTIONS = [
    "summary",         # / objective / profile
    "skills",
    "experience",
    "education",
    "certifications",
    "projects",
    "contact",
]

def _coverage_score(coverage: Dict[str, bool]) -> float:
    """
    Simple coverage: percent of EXPECTED_SECTIONS that are present.
    Returns 0..100.
    """
    if not coverage:
        return 0.0
    total = len(EXPECTED_SECTIONS)
    have = sum(1 for s in EXPECTED_SECTIONS if coverage.get(s, False))
    return 100.0 * have / total if total else 0.0

def structure_score_from_coverage(coverage: Dict[str, bool]) -> float:
    """
    Legacy helper kept for backward compatibility.
    """
    return round(_coverage_score(coverage), 1)


def structure_score(fields: Dict[str, Any], coverage: Dict[str, bool]) -> float:
    """
    Primary structure score used by the API.
    Combines section coverage with a few lightweight heuristics based on extracted fields.

    Inputs:
      fields: {
        "skills": List[str],
        "experienceYears": float|int|None,
        "education": str|dict|None,
        "certifications": List[str],
        "projectsCount": int|None,
        "jobRole": str|None,
        ...
      }
      coverage: Dict[str, bool] (which sections detected)

    Output:
      float in [0, 100]
    """
    score = _coverage_score(coverage)  # base out of 100 (percent of sections present)

    # Heuristic boosts (bounded so total stays in 0..100)
    skills = fields.get("skills") or []
    if isinstance(skills, (list, tuple)):
        if len(skills) >= 5:
            score += 6
        elif len(skills) >= 3:
            score += 3

    exp_years = fields.get("experienceYears")
    try:
        exp_years = float(exp_years) if exp_years is not None else 0.0
    except Exception:
        exp_years = 0.0
    if exp_years >= 5:
        score += 6
    elif exp_years >= 1:
        score += 3

    projects = fields.get("projectsCount")
    try:
        projects = int(projects) if projects is not None else 0
    except Exception:
        projects = 0
    if projects >= 3:
        score += 5
    elif projects >= 1:
        score += 3

    certs = fields.get("certifications") or []
    if isinstance(certs, (list, tuple)) and len(certs) >= 1:
        score += 3

    # Make sure score is within bounds
    if score < 0:
        score = 0.0
    if score > 100:
        score = 100.0

    return round(score, 1)


__all__ = ["structure_score", "structure_score_from_coverage", "EXPECTED_SECTIONS"]
