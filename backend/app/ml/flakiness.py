from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.models.failure import Failure
from app.models.run import Run
from app.models.flakiness import Flakiness

DEFAULT_WINDOW_DAYS = 30


class FlakinessEngine:

    def __init__(self, window_days: int = DEFAULT_WINDOW_DAYS):
        self.window_days = window_days

    def calculate_flakiness(self, db: Session):
        """
        Recalculate flakiness score for all tests within time window.
        Uses Run.finished_at as the time reference.
        """

        since = datetime.utcnow() - timedelta(days=self.window_days)

        # 1. Fetch all runs in window
        recent_runs_subq = (
            db.query(Run.id)
            .filter(
                # If finished_at is NULL (rare), fallback using started_at
                or_(
                    and_(Run.finished_at != None, Run.finished_at >= since),
                    and_(Run.finished_at == None, Run.started_at != None, Run.started_at >= since),
                )
            )
            .subquery()
        )

        # 2. Failures per test_name
        fail_counts = (
            db.query(Failure.test_name, func.count(Failure.id))
            .filter(Failure.run_id.in_(recent_runs_subq))
            .group_by(Failure.test_name)
            .all()
        )

        fail_map = {test: count for test, count in fail_counts}

        # We infer tests from failure history
        test_names = set(fail_map.keys())

        flakiness_records = []

        # Calculation logic
        for test_name in test_names:
            failures = fail_map.get(test_name, 0)

            # We don't know successes because success = run did not report a failure for that test.
            # This will improve once you store per-test results from Jenkins.
            successes = 0

            # Laplace smoothing to avoid extremes
            a = 1
            b = 2

            flakiness_score = (failures + a) / (failures + successes + b)

            flakiness_records.append({
                "test_name": test_name,
                "failures": failures,
                "successes": successes,
                "score": round(flakiness_score, 3)
            })

            # Upsert
            row = db.query(Flakiness).filter(
                Flakiness.test_name == test_name
            ).first()

            if not row:
                row = Flakiness(
                    test_name=test_name,
                    success_count=successes,
                    failure_count=failures,
                    flakiness_score=flakiness_score
                )
                db.add(row)
            else:
                row.success_count = successes
                row.failure_count = failures
                row.flakiness_score = flakiness_score

        db.commit()

        return flakiness_records