import os
import pathlib
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Resolve project root (directory containing app.py)
ROOT = pathlib.Path(__file__).resolve().parent
os.chdir(ROOT)  # make relative paths predictable

# Local imports (no package-prefix needed)
from services.extract import extract_text_from_pdf
from services.sectioner import section_resume
from services.features import compute_features
from services.scoring import ScoreEngine
from services.feedback import rule_based_feedback
from services.llm import llm_feedback_if_enabled

load_dotenv()  # load .env

API_TITLE = "HireMe Resume Analyzer API"
app = FastAPI(title=API_TITLE)

# CORS for local dev
origins = [
    os.getenv("FRONTEND_ORIGIN", "http://localhost:5173"),
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model path (absolute)
model_path_env = os.getenv("MODEL_PATH", "models/resume_ai_score_reg_xgb.pkl")
MODEL_PATH = str((ROOT / model_path_env).resolve())

scorer = ScoreEngine(model_path=MODEL_PATH)

class AnalyzeResponse(BaseModel):
    extractedText: str
    sections: dict
    features: dict
    score: int
    modelUsed: str
    feedback: dict

@app.get("/health")
def health():
    return {"ok": True, "modelLoaded": scorer.model_loaded}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    file: UploadFile = File(...),
    generate_llm: bool = Form(False),
):
    # 1) extract + clean
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    # 2) sectioning
    sections = section_resume(text)

    # 3) features
    feats = compute_features(text=text, sections=sections)

    # 4) scoring
    score, model_used = scorer.score(feats, sections)

    # 5) feedback
    feedback_dict = {
        "ruleBased": rule_based_feedback(feats, sections),
        "llm": []
    }
    if generate_llm:
        feedback_dict["llm"] = llm_feedback_if_enabled(sections, feats, score)

    return {
        "extractedText": text,
        "sections": sections,
        "features": feats,
        "score": score,
        "modelUsed": model_used,
        "feedback": feedback_dict
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
