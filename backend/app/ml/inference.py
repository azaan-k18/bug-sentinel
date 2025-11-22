from typing import Tuple, Dict
from app.core.config import settings
from .model_loader import load_tfidf_and_model
import numpy as np

TFIDF, MODEL = load_tfidf_and_model(settings.MODEL_PATH)

def predict_label(text: str) -> Dict:
    """
    Return {label, confidence}. If model unavailable, return fallback.
    """
    if TFIDF is None or MODEL is None:
        # fallback heuristic
        lower = (text or "").lower()
        if "timeout" in lower or "timed out" in lower:
            return {"label": "infra", "confidence": 0.6}
        if "nosuchelement" in lower or "no such element" in lower or "selector" in lower:
            return {"label": "locator", "confidence": 0.7}
        return {"label": "other", "confidence": 0.5}
    vec = TFIDF.transform([text])
    probs = MODEL.predict_proba(vec)[0]
    idx = int(np.argmax(probs))
    label = MODEL.classes_[idx]
    confidence = float(probs[idx])
    return {"label": label, "confidence": confidence}
