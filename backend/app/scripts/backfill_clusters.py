import json
from app.db.session import SessionLocal

# IMPORTANT: load all models before referencing any model classes
import app.db.base_models

from app.models.failure import Failure
from app.models.cluster import Cluster
from app.ml.clusterer import Clusterer


def run_backfill():
    db = SessionLocal()

    failures = db.query(Failure).filter(Failure.cluster_id == None).all()
    print(f"Failures to cluster: {len(failures)}")

    clusterer = Clusterer()

    for f in failures:
        cluster_id, created_new = clusterer.assign_to_cluster(
            db,
            Failure,
            Cluster,
            f,
            threshold=0.65
        )
        print(f"Assigned failure {f.id} → cluster {cluster_id} (new={created_new})")

    db.close()


if __name__ == "__main__":
    run_backfill()
