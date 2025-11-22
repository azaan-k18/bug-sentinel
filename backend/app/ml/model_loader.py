import os
import joblib

def load_tfidf_and_model(model_dir: str):
    tfidf_path = os.path.join(model_dir, "tfidf.joblib")
    xgb_path = os.path.join(model_dir, "xgb_model.joblib")
    tfidf = None
    model = None
    if os.path.exists(tfidf_path) and os.path.exists(xgb_path):
        tfidf = joblib.load(tfidf_path)
        model = joblib.load(xgb_path)
    return tfidf, model
