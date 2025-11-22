# app/api/v1/groups.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.session import get_db
from app.models.cluster import Cluster
from app.models.failure import Failure

router = APIRouter(prefix="/groups", tags=["groups"])

@router.get("/")
def list_groups(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    clusters = db.query(Cluster).order_by(Cluster.member_count.desc()).offset(offset).limit(limit).all()
    out = []
    for c in clusters:
        # fetch top 5 failures for preview
        members = db.query(Failure).filter(Failure.cluster_id == c.id).order_by(Failure.id.desc()).limit(5).all()
        out.append({
            "cluster_id": c.id,
            "representative_message": c.representative_message,
            "member_count": c.member_count,
            "members_preview": [{"failure_id": m.id, "test_name": m.test_name, "normalized": m.error_message} for m in members]
        })
    return {"total": len(out), "clusters": out}

@router.get("/{cluster_id}")
def get_cluster(cluster_id: int, db: Session = Depends(get_db)):
    c = db.query(Cluster).filter(Cluster.id == cluster_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cluster not found")
    members = db.query(Failure).filter(Failure.cluster_id == c.id).all()
    return {
        "cluster_id": c.id,
        "representative_message": c.representative_message,
        "member_count": c.member_count,
        "members": [{"failure_id": m.id, "test_name": m.test_name, "normalized": m.error_message} for m in members]
    }