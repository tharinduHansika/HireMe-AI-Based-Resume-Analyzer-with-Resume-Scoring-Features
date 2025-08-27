# core/model_adapter.py
import numpy as np
import pandas as pd
from typing import Tuple

def _row_from_extracted(extracted: dict) -> pd.DataFrame:
    skills_text = ", ".join(extracted.get("skills", [])) if extracted.get("skills") else ""
    education   = extracted.get("education") or ""
    certs       = extracted.get("certifications", [])
    certs_text  = ", ".join(certs) if certs else "No Certification"
    job_role    = extracted.get("jobRole") or ""
    exp_years   = float(extracted.get("experienceYears") or 0.0)
    projects    = int(extracted.get("projectsCount") or 0)

    row = {
        "Skills": skills_text,
        "Education": education,
        "Certifications": certs_text,
        "Job Role": job_role,
        "Experience (Years)": exp_years,
        "Projects Count": projects,
    }
    return pd.DataFrame([row])

def predict_ai_score_regression(pipeline, extracted: dict) -> Tuple[float, dict]:
    X = _row_from_extracted(extracted)
    y = float(pipeline.predict(X)[0])
    y = float(np.clip(y, 0.0, 100.0))
    return y, X.to_dict(orient="records")[0]
