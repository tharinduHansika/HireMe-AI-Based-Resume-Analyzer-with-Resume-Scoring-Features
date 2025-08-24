def structure_score_from_coverage(coverage: dict) -> float:
    """
    Start at 100; subtract points for missing sections.
    Hard penalties for core sections; soft for optional ones.
    """
    score = 100.0
    # Core
    if not coverage.get("skills"): score -= 20
    if not coverage.get("experience"): score -= 20
    if not coverage.get("education"): score -= 20
    # Optional
    if not coverage.get("projects"): score -= 10
    if not coverage.get("certifications"): score -= 10
    if not coverage.get("summary"): score -= 10
    if not coverage.get("contact"): score -= 10
    return float(max(0.0, min(100.0, score)))

def blend_final_score(ml_score: float, structure_score: float, w_ml: float = 0.7) -> float:
    w_ml = max(0.0, min(1.0, w_ml))
    w_st = 1.0 - w_ml
    final = w_ml * ml_score + w_st * structure_score
    return float(max(0.0, min(100.0, final)))
