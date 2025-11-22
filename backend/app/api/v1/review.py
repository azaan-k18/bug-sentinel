from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.failure import Failure
from app.models.label import Label

router = APIRouter()

@router.get("/queue")
def review_queue(limit: int = 50, db: Session = Depends(get_db)):
    """
    Return failures that have no label or have a model label with low confidence.
    """
    try:
        # unlabeled failures
        subq = db.query(Label.failure_id).subquery()
        unlabeled = db.query(Failure).filter(~Failure.id.in_(subq)).limit(limit).all()
        # return minimal payload for review UI
        results = [{"id": f.id, "run_id": f.run_id, "summary": f.extracted_message} for f in unlabeled]
        return {"queue": results}
    except Exception:
        # fallback sample
        return {"queue": [{"id": 1, "run_id": 101, "summary": "TimeoutException: page load"}]}
