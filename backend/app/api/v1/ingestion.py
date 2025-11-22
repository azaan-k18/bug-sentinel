from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.db.session import get_db
from app.parsers.jenkins_parser import extract_failures_from_console
from app.models.run import Run
from app.models.failure import Failure

router = APIRouter()

class JenkinsPayload(BaseModel):
    metadata: Dict[str, Any]
    log: str

@router.post("/jenkins")
def ingest_jenkins(payload: JenkinsPayload, db: Session = Depends(get_db)):
    """
    Ingest a Jenkins job console log (or POSTed artifact). Parser extracts failure nodes
    and stores Run + Failure rows. ML labeling will be done async later (or during ingest).
    """
    meta = payload.metadata
    log_text = payload.log or ""
    # create run (minimal)
    run = Run(
        website_id = meta.get("website_id"),
        jenkins_server = meta.get("server"),
        job_name = meta.get("job_name") or meta.get("job"),
        build_number = meta.get("build_number"),
        status = meta.get("status")
    )
    db.add(run)
    db.flush()  # assign id without commit

    failures = extract_failures_from_console(log_text)
    created = []
    for f in failures:
        failure = Failure(
            run_id = run.id,
            error_message = f.get("raw"),
            extracted_message = f.get("summary")
        )
        db.add(failure)
        created.append({"summary": f.get("summary")})

    db.commit()
    return {"msg": "ingested", "run_id": run.id, "failures": created}