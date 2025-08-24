import os
import json
import joblib
import numpy as np
from collections import namedtuple

ModelBundle = namedtuple("ModelBundle", ["model", "encoders"])

EDU_MAP = {
    None: 0, "Diploma": 1, "Bachelor": 2, "Bachelors": 2, "BSc": 2, "B.Sc": 2,
    "Master": 3, "MSc": 3, "M.Sc": 3, "PhD": 4, "Doctor": 4
}

def _education_level_from_text(education: str | None) -> int:
    if not education: return 0
    t = education.lower()
    if "phd" in t or "doctor" in t: return 4
    if "master" in t or "msc" in t or "m.sc" in t: return 3
    if "bachelor" in t or "bsc" in t or "b.sc" in t: return 2
    if "diploma" in t or "higher national" in t or "hnc" in t: return 1
    return 0

def load_model_and_encoders(model_path: str, encoders_path: str) -> ModelBundle:
    model = None
    encoders = None
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
        except Exception:
            model = None
    if os.path.exists(encoders_path):
        try:
            encoders = joblib.load(encoders_path)
        except Exception:
            encoders = None
    return ModelBundle(model=model, encoders=encoders)

def build_features(extracted: dict, encoders=None):
    """
    Returns (features_array, feature_vector_dict)
    """
    skills = extracted.get("skills", [])
    exp_years = float(extracted.get("experienceYears") or 0.0)
    education = extracted.get("education")
    certs = extracted.get("certifications", [])
    job_role = extracted.get("jobRole") or ""
    projects = int(extracted.get("projectsCount") or 0)

    skills_count = min(len(skills), 50)
    certifications_count = min(len(certs), 50)
    education_level = _education_level_from_text(education)

    # Base numeric set
    feature_vector = {
        "skills_count": skills_count,
        "experience_years": exp_years,
        "education_level": education_level,
        "certifications_count": certifications_count,
        "projects_count": projects,
        "job_role": job_role or "",
    }

    # Optional: encode job_role using saved encoders
    job_role_code = 0
    if encoders and "job_role_le" in encoders:
        try:
            job_role_code = int(encoders["job_role_le"].transform([job_role])[0])
        except Exception:
            job_role_code = 0

    # Assemble features vector (keep deterministic order)
    features = [
        feature_vector["skills_count"],
        feature_vector["experience_years"],
        feature_vector["education_level"],
        feature_vector["certifications_count"],
        feature_vector["projects_count"],
        job_role_code
    ]

    # Provide a simple heuristic if model is not available
    # (weights are just sensible defaults; tune as you like)
    heuristic = (
        (min(skills_count, 20) / 20) * 35.0 +
        (min(exp_years, 10) / 10) * 30.0 +
        (education_level / 4) * 15.0 +
        (min(certifications_count, 5) / 5) * 10.0 +
        (min(projects, 8) / 8) * 10.0
    )
    feature_vector["_heuristic_ml"] = float(max(0.0, min(100.0, heuristic)))

    return np.array(features, dtype=float), feature_vector
