import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "xgb_model.pkl")

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return None  # dummy fallback
