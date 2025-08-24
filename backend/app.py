import os
import io
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
from werkzeug.utils import secure_filename

from core.parser import extract_text_from_pdf
from core.extractor import extract_structured_fields, detect_section_coverage
from core.featurizer import load_model_and_encoders, build_features
from core.scorer import structure_score_from_coverage, blend_final_score
from core.llm import generate_feedback

load_dotenv()

# ---- Config ----
PORT = int(os.getenv("PORT", "5000"))
MAX_CONTENT_MB = int(os.getenv("MAX_CONTENT_MB", "10"))
MODEL_PATH = os.getenv("MODEL_PATH", "./models/resume_regressor.pkl")
ENCODERS_PATH = os.getenv("ENCODERS_PATH", "./utils/encoders.pkl")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

ALLOWED_EXTENSIONS = {"pdf"}

# ---- Flask ----
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_MB * 1024 * 1024

# ---- Load model & encoders (if present) ----
model_bundle = load_model_and_encoders(MODEL_PATH, ENCODERS_PATH)

# ---- Schemas ----
class AnalyzeRequest(BaseModel):
    job_role: str | None = None
    use_llm: bool = True

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True})

@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    # Parse non-file fields
    job_role = request.form.get("job_role") or None
    use_llm = request.form.get("use_llm", "1") in ("1", "true", "True")

    try:
        _ = AnalyzeRequest(job_role=job_role, use_llm=use_llm)
    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), 400

    # ---- 1) PDF → text
    pdf_bytes = file.read()
    text = extract_text_from_pdf(pdf_bytes)

    # log first 2,000 chars so your terminal doesn't explode
    app.logger.info("EXTRACTED TEXT (first 2000 chars):\n%s", text[:2000])

    # ---- 2) text → structured fields
    extracted = extract_structured_fields(text, fallback_job_role=job_role)

    # ---- 3) section coverage
    coverage = detect_section_coverage(text, extracted)

    # ---- 4) features for model
    features, feature_vector = build_features(extracted, encoders=model_bundle.encoders)

    # ---- 5) ML score (0-100)
    if model_bundle.model is not None:
        try:
            ml_raw = float(model_bundle.model.predict([features])[0])
            ml_score = max(0, min(100, ml_raw))
        except Exception as e:
            # If model fails, use heuristic
            ml_score = feature_vector.get("_heuristic_ml", 50.0)
    else:
        ml_score = feature_vector.get("_heuristic_ml", 50.0)

    # ---- 6) Structure score (0-100)
    structure_score = structure_score_from_coverage(coverage)

    # ---- 7) Final score
    final_score = blend_final_score(ml_score, structure_score)

    # ---- 8) LLM feedback (optional)
    feedback = generate_feedback(
        extracted=extracted,
        coverage=coverage,
        scores={"final": final_score, "ml": ml_score, "structure": structure_score},
        job_role=job_role or extracted.get("jobRole"),
        api_key=OPENAI_API_KEY,
        model_name=OPENAI_MODEL,
    ) if use_llm else []

    # ---- 9) Response
    return jsonify({
        "scores": {"final": round(final_score, 2), "ml": round(ml_score, 2), "structure": round(structure_score, 2)},
        "sectionCoverage": coverage,
        "extracted": extracted,
        "featureVector": {k: (float(v) if isinstance(v, (int, float)) else v) for k, v in feature_vector.items()
                           if not k.startswith("_")},  # hide internal keys
        "llmFeedback": feedback,
    })
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
