import os
import numpy as np
import pandas as pd
import joblib

FEATURE_ORDER = [
    "num_skills","has_education","has_experience","has_contact",
    "num_projects","num_certifications","total_words",
    "readability_flesch","years_experience_est","quantified_achievements"
]

class ScoreEngine:
    def __init__(self, model_path: str | None = None):
        self.model_loaded = False
        self.model = None
        self.model_name = "RuleScore v1.0"
        if model_path and os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                self.model_loaded = True
                self.model_name = "XGBoostRegressor"
            except Exception:
                self.model_loaded = False
                self.model = None

    def _rule_score(self, feats: dict, sections: dict) -> int:
        score = 35
        if feats["has_contact"]: score += 8
        if feats["has_education"]: score += 8
        if feats["has_experience"]: score += 10
        if feats["num_skills"] >= 8: score += 8
        if feats["num_projects"] >= 2: score += 6
        if feats["num_certifications"] >= 1: score += 4

        read = feats["readability_flesch"]
        if 50 <= read <= 70: score += 8
        elif read < 30: score -= 5

        if feats["quantified_achievements"] >= 3: score += 8
        elif feats["quantified_achievements"] == 0: score -= 6

        if feats["years_experience_est"] >= 3: score += 6
        if feats["total_words"] > 900: score -= 5

        return int(max(0, min(100, score)))

    def score(self, feats: dict, sections: dict) -> tuple[int, str]:
        if self.model_loaded and self.model is not None:
            X = pd.DataFrame([[feats.get(k,0) for k in FEATURE_ORDER]], columns=FEATURE_ORDER)
            try:
                y = float(self.model.predict(X)[0])
                return int(max(0, min(100, round(y)))), self.model_name
            except Exception:
                pass
        return self._rule_score(feats, sections), self.model_name
