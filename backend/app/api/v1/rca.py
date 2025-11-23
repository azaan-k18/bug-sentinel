from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict

from app.db.session import get_db
from app.models.cluster import Cluster
from app.models.failure import Failure
from app.models.flakiness import Flakiness
from app.models.label import Label

router = APIRouter(prefix="/rca", tags=["rca"])

@router.get("/cluster/{cluster_id}")
def rca_for_cluster(cluster_id: int, db: Session = Depends(get_db)):
    cluster = db.query(Cluster).filter(Cluster.id == cluster_id).first()
    if not cluster:
        raise HTTPException(404, "Cluster not found")

    # 1) top labels for failures in this cluster (if Label table has labels)
    top_labels = (
        db.query(Label.label, func.count(Label.id).label("cnt"))
          .join(Failure, Failure.id == Label.failure_id)
          .filter(Failure.cluster_id == cluster_id)
          .group_by(Label.label)
          .order_by(func.count(Label.id).desc())
          .limit(5)
          .all()
    )

    # 2) flakiness score for top tests in the cluster (if test_name present)
    tests = (
        db.query(Failure.test_name, func.count(Failure.id).label("cnt"))
          .filter(Failure.cluster_id == cluster_id)
          .group_by(Failure.test_name)
          .order_by(func.count(Failure.id).desc())
          .limit(10)
          .all()
    )

    test_infos = []
    for tname, cnt in tests:
        fl = db.query(Flakiness).filter(Flakiness.test_name == tname).first()
        test_infos.append({"test_name": tname, "failures": cnt, "flakiness": (fl.flakiness_score if fl else None)})

    return {
        "cluster_id": cluster.id,
        "representative_message": cluster.representative_message,
        "member_count": cluster.member_count,
        "top_labels": [{"label": l[0], "count": l[1]} for l in top_labels],
        "top_tests": test_infos
    }