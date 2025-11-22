from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.db.session import get_db
from app.models.run import Run
from app.models.failure import Failure
from app.models.label import Label

from app.parsers.normalize import normalize_message
from app.ml.inference import classify_message

router = APIRouter()

# ------------------------------------------------------
# REQUEST MODELS
# ------------------------------------------------------
class FailureItem(BaseModel):
    test_name: str
    raw_message: str
    platform: str            # "desktop" / "mobile"
    website: str             # domain only (ex: indianexpress.com)


class IngestionRequest(BaseModel):
    run_id: str              # external pipeline run ID
    jenkins_job: str
    website: str             # main website for this run
    failures: List[FailureItem]


# ------------------------------------------------------
# INGEST ENDPOINT
# ------------------------------------------------------
@router.post("/")
def ingest_failure_report(payload: IngestionRequest, db: Session = Depends(get_db)):
    """
    Receives a run + list of failures
    → Normalize, classify, store in DB
    → Returns run info + classification
    """

    # -----------------------------
    # 1. CREATE RUN ENTRY
    # -----------------------------
    run = Run(
        run_uid=payload.run_id,
        job_name=payload.jenkins_job,
        jenkins_server="local",
        website_id=None,     # until Website table integration
        build_number=None,
        status="FAILED",
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    results = []

    # -----------------------------
    # 2. PROCESS EACH FAILURE
    # -----------------------------
    for f in payload.failures:
        try:
            # Normalize message
            normalized = normalize_message(f.raw_message)

            # ML classification
            label, confidence = classify_message(normalized)

            # -----------------------------
            # Create Failure entry
            # -----------------------------
            failure = Failure(
                run_id=run.id,
                test_name=f.test_name,
                platform=f.platform,
                website=f.website,
                error_message=normalized,
                extracted_message=normalized.split(":")[0],  # simple extraction
                website_id=None
            )
            db.add(failure)
            db.commit()
            db.refresh(failure)

            # -----------------------------
            # Create Label entry
            # -----------------------------
            label_row = Label(
                failure_id=failure.id,
                label=label,
                confidence=confidence,
                source="model",
                labeled_by="model_v1"
            )
            db.add(label_row)
            db.commit()

            # Append to response list
            results.append({
                "failure_id": failure.id,
                "test_name": f.test_name,
                "normalized": normalized,
                "label": label,
                "confidence": confidence
            })

        except Exception as e:
            # Log error and continue with next failure
            print(f"[INGEST ERROR] Failed to store failure: {str(e)}")
            continue

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    return {
        "run_internal_id": run.id,
        "external_run_id": payload.run_id,
        "website": payload.website,
        "total_received": len(payload.failures),
        "classified": results
    }
