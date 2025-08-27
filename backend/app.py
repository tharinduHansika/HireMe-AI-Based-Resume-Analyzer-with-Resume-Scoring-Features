# backend/app.py
import os
from typing import Any, Dict, Tuple

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# ---- Core helpers ----
from core.parser_any import extract_text_any                           # text extractor
from core.extractor import extract_structured_fields                   # field extractor
from core.scorer import structure_score_from_coverage                  # returns 0..100
from core.model_adapter import predict_ai_score_regression             # ML regressor wrapper
from core.llm import generate_feedback                                 # optional LLM feedback

load_dotenv()

app = Flask(__name__)
CORS(app)

DEBUG_ON = os.getenv("DEBUG_ON", "0") == "1"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


def _safe_unpack_extract(filename: str, content_type: str, file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
    """
    extract_text_any may return (text, meta) or (text, meta, aux).
    Handle both shapes safely.
    """
    out = extract_text_any(filename=filename, content_type=content_type, file_bytes=file_bytes)
    if isinstance(out, tuple):
        if len(out) >= 2:
            text = out[0]
            meta = out[1] if isinstance(out[1], dict) else {}
            return str(text or ""), dict(meta or {})
        return str(out[0] if out else ""), {}
    return str(out or ""), {}


def _to_ui_fields(fields: Dict[str, Any], job_role: str) -> Dict[str, Any]:
    """Normalize to stable keys for the frontend."""
    def _get_list(key):
        v = fields.get(key, [])
        if isinstance(v, str):
            return [v]
        return v if isinstance(v, list) else []

    def _get_str(key):
        v = fields.get(key, "")
        if isinstance(v, (list, tuple)):
            return ", ".join([str(x) for x in v])
        return str(v or "")

    return {
        "job_role": (job_role or _get_str("target_job_role")),
        "years_experience": float(fields.get("years_experience", 0) or 0),
        "projects_count": int(fields.get("projects_count", 0) or 0),
        "education": _get_list("education"),
        "skills": _get_list("skills"),
        "certifications": _get_list("certifications"),
    }


def _simple_coverage(text: str, fields: Dict[str, Any]) -> Dict[str, bool]:
    """
    Fallback coverage calculator when a dedicated sectionizer isn't available.
    Marks presence/absence of common resume sections using the already-extracted fields.
    """
    candidates = {
        "summary": ("summary", "objective", "about_me", "profile"),
        "experience": ("experience", "work_experience", "employment", "roles"),
        "education": ("education",),
        "skills": ("skills", "technical_skills"),
        "projects": ("projects", "project_experience"),
        "certifications": ("certifications", "certs"),
        "contact": ("contact", "email", "phone", "links"),
    }

    cov: Dict[str, bool] = {}
    text_l = (text or "").lower()

    for sec, keys in candidates.items():
        # present if we have an extracted field OR the word appears in raw text
        present = any(k in fields and fields.get(k) for k in keys) or any(k in text_l for k in keys)
        cov[sec] = bool(present)

    return cov


def _call_predict(fields: Dict[str, Any], job_role: str, return_debug: bool):
    """
    Call predict_ai_score_regression robustly (supports keyword/positional + optional debug).
    """
    try:
        if return_debug:
            return predict_ai_score_regression(fields, job_role=job_role, return_debug=True)
        return predict_ai_score_regression(fields, job_role=job_role)
    except TypeError:
        if return_debug:
            try:
                return predict_ai_score_regression(fields, job_role, True)
            except TypeError:
                score = predict_ai_score_regression(fields, job_role)
                return score, {}
        else:
            return predict_ai_score_regression(fields, job_role)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        # ---- read multipart form ----
        if "file" not in request.files:
            return jsonify({"error": "No file part in form-data"}), 400

        f = request.files["file"]
        if not f or f.filename == "":
            return jsonify({"error": "No selected file"}), 400

        job_role = (request.form.get("job_role") or "").strip()
        use_llm = (request.form.get("use_llm") or "false").lower() == "true"

        file_bytes = f.read()
        text, meta = _safe_unpack_extract(filename=f.filename, content_type=f.content_type or "", file_bytes=file_bytes)

        # ---- extract structured fields ----
        fields = extract_structured_fields(text)
        ui_fields = _to_ui_fields(fields, job_role)

        # ---- structure score ----
        # First try: some implementations accept fields directly
        try:
            structure = float(structure_score_from_coverage(fields))
        except Exception:
            # Fallback: compute a simple coverage dict and try again
            coverage = _simple_coverage(text, fields)
            try:
                structure = float(structure_score_from_coverage(coverage))
            except Exception:
                # Final fallback: ratio of covered sections
                ratio = sum(1 for v in coverage.values() if v) / max(1, len(coverage))
                structure = round(100.0 * ratio, 1)

        # ---- ML score ----
        ml_res = _call_predict(fields, job_role, return_debug=DEBUG_ON)
        if isinstance(ml_res, tuple) and len(ml_res) == 2:
            ml_score, dbg = ml_res
        else:
            ml_score, dbg = ml_res, {}

        ml_score = float(ml_score or 0.0)
        structure = float(structure or 0.0)
        final_score = round(0.7 * ml_score + 0.3 * structure, 1)

        # ---- LLM feedback (optional) ----
        feedback = []
        if use_llm:
            try:
                api_key = os.getenv("OPENAI_API_KEY", "")
                try:
                    feedback = generate_feedback(text=text, job_role=job_role, api_key=api_key)
                except TypeError:
                    feedback = generate_feedback(text)
                if not isinstance(feedback, list):
                    feedback = [str(feedback)]
            except Exception as e:
                feedback = [f"LLM feedback unavailable: {e}"]

        # ---- response ----
        return jsonify({
            "final_score": round(final_score, 1),
            "ml_score": round(ml_score, 1),
            "structure_score": round(structure, 1),
            "extracted": ui_fields,
            "feedback": feedback,
            "debug": dbg if DEBUG_ON else None,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
