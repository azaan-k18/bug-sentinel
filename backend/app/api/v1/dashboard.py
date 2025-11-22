from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.run import Run
from app.models.failure import Failure

router = APIRouter()

@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    """
    Returns a simple overview used by the frontend.
    If DB unavailable or empty, returns sensible defaults.
    """
    # try to gather aggregations - if DB not ready / empty, respond with defaults
    try:
        total_failures = db.query(Failure).count()
        total_runs = db.query(Run).count()
        # pass rate (runs with no failures / total runs)
        runs_with_failures = db.query(Run).join(Failure, Failure.run_id == Run.id).distinct(Run.id).count()
        pass_rate = 0.0
        if total_runs > 0:
            pass_rate = round(((total_runs - runs_with_failures) / total_runs) * 100, 2)
        false_positive_rate = 0.0  # placeholder (requires labeling)
        return {
            "total_bugs": total_failures,
            "total_runs": total_runs,
            "pass_rate": pass_rate,
            "false_positive_rate": false_positive_rate
        }
    except Exception:
        # if DB not connected or query fails, return dummy values
        return {
            "total_bugs": 0,
            "total_runs": 0,
            "pass_rate": 100.0,
            "false_positive_rate": 0.0
        }

@router.get("/by-website")
def by_website(db: Session = Depends(get_db)):
    # sample aggregation: failures grouped by website_id
    try:
        rows = db.query(Failure.website_id, Failure.extracted_message).all()
        # quick group
        counts = {}
        for w_id, _ in rows:
            key = w_id or "unknown"
            counts[key] = counts.get(key, 0) + 1
        return {"by_website": counts}
    except Exception:
        return {"by_website": {}}
