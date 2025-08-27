# app.py
import os
import io
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError

from core.parser import extract_text_from_pdf
from core.extractor import extract_structured_fields, detect_section_coverage
from core.scorer import structure_score_from_coverage  # we keep structure score
from core.llm import generate_feedback

from core.featurizer import load_model_and_encoders
from core.model_adapter import predict_ai_score_regression

load_dotenv()

PORT = int(os.getenv("PORT", "5000"))
MAX_CONTENT_MB = int(os.getenv("MAX_CONTENT_MB", "10"))
MODEL_PATH = os.getenv("MODEL_PATH", "./models/resume_ai_score_reg_xgb.pkl")
ENCODERS_PATH = os.getenv("ENCODERS_PATH", "./utils/encoders.pkl")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_MB * 1024 * 1024

# Load the saved regression pipeline (with strong diagnostics)
model_bundle = load_model_and_encoders(MODEL_PATH, ENCODERS_PATH)
if model_bundle.error:
    app.logger.warning(f"Model load warning: {model_bundle.error}")
app.logger.info(f"Model path (abs): {model_bundle.model_path_abs} ; loaded={model_bundle.model is not None}")

class AnalyzeRequest(BaseModel):
    job_role: str | None = None
    use_llm: bool = True

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "model_loaded": model_bundle.model is not None, "model_path": model_bundle.model_path_abs})

@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    job_role = request.form.get("job_role") or None
    use_llm  = request.form.get("use_llm", "1") in ("1", "true", "True")

    try:
        _ = AnalyzeRequest(job_role=job_role, use_llm=use_llm)
    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), 400

    # Ensure model is loaded
    if model_bundle.model is None:
        return jsonify({
            "error": "Model file not loaded. Check MODEL_PATH.",
            "debug": {
                "model_path_abs": model_bundle.model_path_abs,
                "load_error": model_bundle.error
            }
        }), 500

    # 1) PDF → text
    pdf_bytes = file.read()
    text = extract_text_from_pdf(pdf_bytes)
    app.logger.info(f"Extracted text length: {len(text)}")

    # 2) text → structured fields
    extracted = extract_structured_fields(text, fallback_job_role=job_role)

    # 3) section coverage
    coverage = detect_section_coverage(text, extracted)

    # 4) Model prediction (0..100)
    try:
        ml_score, row_used = predict_ai_score_regression(model_bundle.model, extracted)
    except Exception as e:
        app.logger.exception("Model inference failed")
        return jsonify({
            "error": f"Model inference failed: {type(e).__name__}: {e}",
            "debug": {"model_path_abs": model_bundle.model_path_abs}
        }), 500

    # 5) Structure score & Final
    structure_score = structure_score_from_coverage(coverage)
    final_score = ml_score  # AI Score = model score

    # 6) Optional LLM feedback
    feedback = generate_feedback(
        extracted=extracted,
        coverage=coverage,
        scores={"final": final_score, "ml": ml_score, "structure": structure_score},
        job_role=job_role or extracted.get("jobRole"),
        api_key=OPENAI_API_KEY,
        model_name=OPENAI_MODEL,
    ) if use_llm else []

    # 7) Response
    return jsonify({
        "scores": {
            "final": round(final_score, 2),
            "ml": round(ml_score, 2),
            "structure": round(structure_score, 2)
        },
        "sectionCoverage": coverage,
        "extracted": extracted,
        "featureVector": row_used,      # what we fed into your pipeline
        "llmFeedback": feedback,
        "debug": {
            "modelUsed": "regression_pipeline",
            "model_path_abs": model_bundle.model_path_abs,
            "model_load_error": model_bundle.error
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
