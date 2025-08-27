# backend/core/model_adapter.py
# Glue code that loads your trained regression pipeline and serves predictions.

from __future__ import annotations

import os
import pickle
from typing import Dict, Any, Tuple, Optional

import numpy as np
import pandas as pd

# Read once at import
MODEL_PATH = os.getenv("MODEL_PATH", "./models/resume_ai_score_reg_xgb.pkl")

_MODEL = None  # lazy-loaded global


def _get_model():
    """
    Lazy-load the pickled regression pipeline once.
    """
    global _MODEL
    if _MODEL is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"MODEL_PATH not found: {MODEL_PATH}")
        with open(MODEL_PATH, "rb") as f:
            _MODEL = pickle.load(f)
    return _MODEL


# Columns expected by your training pipeline (safe defaults if missing)
_EXPECTED_COLS = [
    "Skills",
    "Education",
    "Certifications",
    "Job Role",
    "Experience (Years)",
    "Projects Count",
]


def _to_model_row(fields: Dict[str, Any], job_role: Optional[str]) -> pd.DataFrame:
    """
    Normalize extracted `fields` into the exact schema your pipeline expects.
    `job_role` from the UI can override the detected field.
    """
    # Safe gets
    skills = fields.get("skills") or fields.get("Skills") or ""
    # If a list came through, join to a single string
    if isinstance(skills, (list, tuple, set)):
        skills = ", ".join([str(s) for s in skills])

    education = fields.get("education") or fields.get("Education") or ""
    certs = fields.get("certifications") or fields.get("Certifications") or ""
    if isinstance(certs, (list, tuple, set)):
        certs = ", ".join([str(c) for c in certs])

    jr = job_role if (job_role and job_role.strip()) else (
        fields.get("target_job_role")
        or fields.get("Job Role")
        or fields.get("job_role")
        or ""
    )

    exp_years = fields.get("experience_years") or fields.get("Experience (Years)") or 0
    proj_count = fields.get("projects_count") or fields.get("Projects Count") or 0

    # Make sure numeric fields are numeric
    try:
        exp_years = float(exp_years)
    except Exception:
        exp_years = 0.0
    try:
        proj_count = int(proj_count)
    except Exception:
        proj_count = 0

    row = {
        "Skills": str(skills),
        "Education": str(education),
        "Certifications": str(certs),
        "Job Role": str(jr),
        "Experience (Years)": exp_years,
        "Projects Count": proj_count,
    }

    # Ensure all expected columns exist (some pipelines are strict)
    for c in _EXPECTED_COLS:
        row.setdefault(c, "" if c not in ["Experience (Years)", "Projects Count"] else 0)

    return pd.DataFrame([row], columns=_EXPECTED_COLS)


def predict_ai_score_regression(
    fields: Dict[str, Any],
    job_role: Optional[str] = None,
    return_debug: bool = False,
) -> float | Tuple[float, Dict[str, Any]]:
    """
    Predict AI score [0..100] using your saved regression pipeline.
    Accepts `job_role` (optional) so the caller can override/augment features.

    Returns:
        score or (score, debug_dict) if `return_debug=True`
    """
    model = _get_model()
    X = _to_model_row(fields, job_role)
    raw = model.predict(X)[0]
    score = float(np.round(np.clip(raw, 0, 100), 1))

    if return_debug:
        return score, {
            "model_path": os.path.abspath(MODEL_PATH),
            "model_type": type(model).__name__,
            "features": X.to_dict(orient="records")[0],
            "raw_pred": float(raw),
        }
    return score
