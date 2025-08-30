# backend/app.py
import os
import math
from typing import Any, Dict, Tuple, Union

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# ---- Core helpers (must exist in backend/core) -----------------------------
from core.parser_any import extract_text_any                   # text extractor
from core.extractor import extract_structured_fields           # structured fields
from core.sectionizer import detect_section_coverage           # structure coverage
from core.model_adapter import predict_ai_score_regression     # ML score adapter
from core.llm import generate_feedback                         # optional LLM advice

# ---------------------------------------------------------------------------

load_dotenv()

app = Flask(__name__)
# CORS for local dev; tighten for prod if needed
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


# ---------------------------- small utilities -------------------------------

def _bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    s = str(v or "").strip().lower()
    return s in {"1", "true", "yes", "y", "on"}

def _safe_float(x: Any, default=0.0) -> float:
    try:
        return float(x)
    except Exception:
        return float(default)

def _to_ui_fields(fields: Dict[str, Any], job_role: str) -> Dict[str, Any]:
    """
    Normalize extracted fields for the UI.
    Only includes keys the UI actually renders.
    """
    edu = fields.get("education") or fields.get("education_entries") or []
    if isinstance(edu, str):
        edu = [edu]

    skills = fields.get("skills") or []
    if isinstance(skills, str):
        # Some extractors return a space- or comma-separated string
        skills = [s.strip() for s in skills.replace(";", ",").split(",") if s.strip()]

    exp_years = fields.get("experience_years")
    if isinstance(exp_years, (list, tuple)) and exp_years:
        exp_years = exp_years[0]
    exp_years = _safe_float(exp_years, 0)

    projects = fields.get("projects_count")
    try:
        projects = int(projects)
    except Exception:
        projects = 0

    certs = fields.get("certifications") or []
    if isinstance(certs, str):
        certs = [certs]

    return {
        "job_role": (job_role or fields.get("job_role") or "").strip(),
        "education": edu,
        "skills": skills,
        "experience_years": exp_years,
        "projects_count": projects,
        "certifications": certs,
    }

def _structure_score_from_coverage(text_or_fields: Union[str, Dict[str, Any]]) -> Tuple[float, Dict[str, Any]]:
    """
    `detect_section_coverage` may return either a float or (float, details).
    Normalize to (score_0_to_100, details_dict).
    """
    cov = detect_section_coverage(text_or_fields)
    if isinstance(cov, tuple) and len(cov) >= 1:
        score = _safe_float(cov[0], 0)
        details = cov[1] if len(cov) > 1 and isinstance(cov[1], dict) else {}
    else:
        score = _safe_float(cov, 0)
        details = {}
    # clamp
    score = max(0.0, min(100.0, score))
    return score, details

def _call_predict_adapter(fields: Dict[str, Any], job_role: str, debug_on: bool) -> Tuple[float, Any]:
    """
    Be tolerant of different adapter signatures.
    Returns (score, debug_or_None).
    """
    try:
        if debug_on:
            out = predict_ai_score_regression(fields, job_role=job_role, return_debug=True)
        else:
            out = predict_ai_score_regression(fields, job_role=job_role)
    except TypeError:
        # Older signature without job_role
        if debug_on:
            out = predict_ai_score_regression(fields, True)  # many adapters use (fields, return_debug)
        else:
            out = predict_ai_score_regression(fields)

    if isinstance(out, tuple) and len(out) == 2:
        score, dbg = out
    else:
        score, dbg = out, None

    try:
        score = float(score)
    except Exception:
        score = 0.0

    # clamp for sanity
    score = max(0.0, min(100.0, score))
    return score, dbg

# ------------------------------ routes --------------------------------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"ok": True})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        # ---- read request ---------------------------------------------------
        use_llm = _bool(request.form.get("use_llm", "false"))
        job_role = (request.form.get("job_role") or "").strip()
        debug_on = _bool(os.getenv("DEBUG_ANALYZE", "false"))

        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file part in form-data"}), 400

        raw_bytes = file.read() or b""
        if not raw_bytes:
            return jsonify({"error": "Uploaded file is empty"}), 400

        # ---- extract text & fields -----------------------------------------
        text, meta = extract_text_any(
            filename=file.filename or "",
            content_type=file.content_type or "",
            file_bytes=raw_bytes,
        )

        fields = extract_structured_fields(text) or {}
        ui_fields = _to_ui_fields(fields, job_role)

        # ---- structure score ------------------------------------------------
        structure, structure_dbg = _structure_score_from_coverage(fields)

        # ---- ML score -------------------------------------------------------
        ml_score, model_dbg = _call_predict_adapter(fields, job_role, debug_on)

        # ---- final score (rounded) -----------------------------------------
        final_score = round(0.7 * ml_score + 0.3 * structure, 1)

        # ---- optional LLM feedback -----------------------------------------
        feedback = []
        if use_llm:
            try:
                api_key = os.getenv("OPENAI_API_KEY", "")
                # Prefer explicit args (your earlier error showed these were required)
                fb = generate_feedback(text=text, job_role=job_role, api_key=api_key)
                # normalize to list
                if isinstance(fb, str):
                    feedback = [fb]
                elif isinstance(fb, list):
                    feedback = [str(x) for x in fb]
                else:
                    feedback = [str(fb)]
            except TypeError:
                # Backward-compat: older signature generate_feedback(text)
                try:
                    fb = generate_feedback(text)
                    feedback = fb if isinstance(fb, list) else [str(fb)]
                except Exception as e:
                    feedback = [f"LLM feedback unavailable: {e}"]
            except Exception as e:
                feedback = [f"LLM feedback unavailable: {e}"]

        # ---- build response -------------------------------------------------
        resp = {
            "final_score": round(final_score, 1),
            "ml_score": round(ml_score, 1),
            "structure_score": round(structure, 1),
            "extracted": ui_fields,             # normalized keys for UI
            "feedback": feedback,
            "meta": meta,                       # optional, can help debugging parsing
        }

        if debug_on:
            resp["debug"] = {
                "sectionizer": structure_dbg,
                "model": model_dbg,
                "raw_fields": fields,
            }

        return jsonify(resp)

    except Exception as e:
        # Return a compact, debuggable error to frontend
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Use the port your frontend expects (proxy points to 5000)
    app.run(host="0.0.0.0", port=5000, debug=False)
