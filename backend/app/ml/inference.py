from .model_loader import load_model
import random

model = load_model()

dummy_labels = [
    "locator_failure",
    "timeout_error",
    "assertion_failure",
    "network_error",
    "application_crash",
    "environment_issue"
]

def classify_message(message: str):
    """
    If real ML exists → use it.
    Otherwise produce realistic dummy prediction.
    """

    if model:
        pred = model.predict([message])[0]
        conf = max(model.predict_proba([message])[0])
        return pred, float(conf)

    # DUMMY fallback
    label = random.choice(dummy_labels)
    confidence = round(random.uniform(0.4, 0.95), 3)

    return label, confidence
