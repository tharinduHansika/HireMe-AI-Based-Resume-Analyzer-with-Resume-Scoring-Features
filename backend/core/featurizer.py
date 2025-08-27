# core/featurizer.py
import os
import joblib
import pickle
from collections import namedtuple

ModelBundle = namedtuple("ModelBundle", ["model", "encoders", "error", "model_path_abs"])

def _try_joblib(path):
    try:
        return joblib.load(path), None
    except Exception as e:
        return None, f"joblib_load_error: {type(e).__name__}: {e}"

def _try_pickle(path):
    try:
        with open(path, "rb") as f:
            obj = pickle.load(f)
        return obj, None
    except Exception as e:
        return None, f"pickle_load_error: {type(e).__name__}: {e}"

def load_model_and_encoders(model_path: str, encoders_path: str):
    """
    Loads the main model (regression pipeline) and optional encoders.
    Tries joblib first, then pickle. Returns ModelBundle(model, encoders, error, abs_path).
    """
    abs_model_path = os.path.abspath(model_path)
    model, encoders, error = None, None, None

    if not os.path.exists(model_path):
        error = f"model_not_found: {abs_model_path}"
        return ModelBundle(None, None, error, abs_model_path)

    # Try joblib then pickle
    model, err1 = _try_joblib(model_path)
    if model is None:
        model, err2 = _try_pickle(model_path)
        if model is None:
            error = f"{err1} ; {err2}"

    # Encoders are optional/not used now; attempt load only if present
    if os.path.exists(encoders_path):
        try:
            encoders = joblib.load(encoders_path)
        except Exception:
            try:
                with open(encoders_path, "rb") as f:
                    encoders = pickle.load(f)
            except Exception:
                encoders = None

    return ModelBundle(model, encoders, error, abs_model_path)
