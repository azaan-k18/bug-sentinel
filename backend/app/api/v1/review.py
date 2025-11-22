from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.failure import Failure
from app.models.label import Label

router = APIRouter()

#review queue get api
@router.get("/queue")
def review_queue(limit: int = 50, db: Session = Depends(get_db)):
    """
    Returns failures that:
    - Do NOT have a human label yet
    OR
    - Have only model labels with low confidence (< 0.6)
    """

    # Get failures that already have a human label
    human_labeled_fail_ids = db.query(Label.failure_id).filter(
        Label.source == "human"
    ).subquery()

    # Get model labels for low confidence
    low_conf_ids = db.query(Label.failure_id).filter(
        Label.source == "model",
        Label.confidence < 0.6
    ).subquery()

    # Failures requiring review:
    q = db.query(Failure).filter(
        ~Failure.id.in_(human_labeled_fail_ids)      # no human label yet
    ).filter(
        Failure.id.in_(low_conf_ids) | True          # OR low model confidence
    ).order_by(Failure.id.desc()).limit(limit)

    results = []
    for f in q.all():
        results.append({
            "id": f.id,
            "test_name": f.test_name,
            "summary": f.extracted_message,
        })

    return {"queue": results}


#this will fetch single failures
@router.get("/{failure_id}")
def review_get_failure(failure_id: int, db: Session = Depends(get_db)):
    f = db.query(Failure).filter(Failure.id == failure_id).first()
    if not f:
        raise HTTPException(404, "Failure not found")

    # Fetch model label
    model_label = db.query(Label).filter(
        Label.failure_id == failure_id,
        Label.source == "model"
    ).first()

    return {
        "id": f.id,
        "test_name": f.test_name,
        "platform": f.platform,
        "website": f.website,
        "error_message": f.error_message,
        "normalized": f.error_message,
        "model_label": model_label.label if model_label else None,
        "model_confidence": model_label.confidence if model_label else None
    }


#this will post human lables
@router.post("/{failure_id}/label")
def review_save_label(
    failure_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    f = db.query(Failure).filter(Failure.id == failure_id).first()
    if not f:
        raise HTTPException(404, "Failure not found")

    label = payload.get("label")
    reviewer = payload.get("reviewer", "unknown")
    notes = payload.get("notes", "")

    if not label:
        raise HTTPException(400, "Label is required")

    # Insert new human label into Label table
    human_label = Label(
        failure_id=failure_id,
        label=label,
        confidence=1.0,
        source="human",
        labeled_by=reviewer,
        notes=notes
    )

    db.add(human_label)
    db.commit()

    return {"status": "ok", "failure_id": failure_id, "human_label": label}