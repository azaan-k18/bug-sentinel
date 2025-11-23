from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import timedelta

from app.db.session import get_db
from app.models.cluster import Cluster
from app.models.trend import ClusterTrend
from app.models.flakiness import Flakiness
from app.models.failure import Failure

router = APIRouter(prefix="/trends", tags=["trends"])

@router.get("/clusters", response_model=List[Dict])
def list_cluster_trends(db: Session = Depends(get_db), days: int = 30, limit: int = 50):
    """
    Return top clusters sorted by recent spike / trend score.
    """
    # recent date
    row = db.query(ClusterTrend).order_by(ClusterTrend.date.desc()).first()
    if not row:
        return []

    recent_date = row.date
    q = (
        db.query(ClusterTrend.cluster_id,
                 Cluster.representative_message,
                 func.sum(ClusterTrend.failure_count).label("total_failures"),
                 func.max(ClusterTrend.trend_score).label("max_trend"),
                 func.max(ClusterTrend.spike_flag).label("has_spike"))
        .join(Cluster, Cluster.id == ClusterTrend.cluster_id)
        .filter(ClusterTrend.date >= recent_date - timedelta(days=days))
        .group_by(ClusterTrend.cluster_id, Cluster.representative_message)
        .order_by(func.max(ClusterTrend.spike_flag).desc(), func.sum(ClusterTrend.failure_count).desc())
        .limit(limit)
    )
    out = []
    for r in q:
        out.append({
            "cluster_id": r.cluster_id,
            "representative_message": r.representative_message,
            "total_failures": int(r.total_failures),
            "max_trend": float(r.max_trend or 0),
            "has_spike": bool(r.has_spike)
        })
    return out


@router.get("/clusters/{cluster_id}")
def get_cluster_trend(cluster_id: int, db: Session = Depends(get_db)):
    c = db.query(Cluster).filter(Cluster.id == cluster_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cluster not found")

    rows = (
        db.query(ClusterTrend)
        .filter(ClusterTrend.cluster_id == cluster_id)
        .order_by(ClusterTrend.date.asc())
        .all()
    )

    timeseries = [{"date": r.date.isoformat(), "count": r.failure_count,
                   "moving_avg_7d": r.moving_avg_7d, "moving_avg_30d": r.moving_avg_30d,
                   "trend_score": r.trend_score, "spike": bool(r.spike_flag)} for r in rows]

    return {
        "cluster_id": c.id,
        "representative_message": c.representative_message,
        "member_count": c.member_count,
        "timeseries": timeseries
    }


@router.get("/spikes")
def list_spikes(db: Session = Depends(get_db), recent_days: int = 7):
    """
    List clusters that had spikes in the last `recent_days`.
    """
    latest_date_row = db.query(ClusterTrend).order_by(ClusterTrend.date.desc()).first()
    if not latest_date_row:
        return {"spikes": []}

    recent_date = latest_date_row.date - timedelta(days=recent_days)
    q = db.query(ClusterTrend).filter(ClusterTrend.date >= recent_date, ClusterTrend.spike_flag == 1).all()
    out = []
    for r in q:
        c = db.query(Cluster).filter(Cluster.id == r.cluster_id).first()
        out.append({
            "cluster_id": r.cluster_id,
            "date": r.date.isoformat(),
            "failure_count": r.failure_count,
            "representative_message": c.representative_message if c else None
        })
    return {"spikes": out}
