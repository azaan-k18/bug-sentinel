from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.failure import Failure

router = APIRouter()

@router.get("/", response_model=List[dict])
def list_failures(limit: int = 50, db: Session = Depends(get_db)):
    items = db.query(Failure).order_by(Failure.id.desc()).limit(limit).all()
    return [{"id": f.id, "run_id": f.run_id, "summary": f.extracted_message} for f in items]

@router.get("/{failure_id}")
def get_failure(failure_id: int, db: Session = Depends(get_db)):
    f = db.query(Failure).filter(Failure.id == failure_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="failure not found")
    return {
        "id": f.id,
        "run_id": f.run_id,
        "error_message": f.error_message,
        "extracted_message": f.extracted_message
    }
