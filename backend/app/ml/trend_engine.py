from datetime import datetime, timedelta
from collections import defaultdict

from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date, and_, or_

from app.models.failure import Failure
from app.models.cluster import Cluster
from app.models.trend import ClusterTrend
from app.models.run import Run


class TrendEngine:

    def __init__(self, days=60):
        self.days = days

    def compute_daily_trends(self, db: Session):
        """
        Computes daily cluster failure counts using Run.finished_at
        (or Run.started_at if finished_at is missing).
        """

        since = datetime.utcnow() - timedelta(days=self.days)

        # 1. Aggregate failures per day per cluster
        rows = (
            db.query(
                Failure.cluster_id,
                cast(Run.finished_at, Date).label("day"),
                func.count(Failure.id)
            )
            .join(Run, Run.id == Failure.run_id)
            .filter(
                or_(
                    and_(Run.finished_at != None, Run.finished_at >= since),
                    and_(Run.finished_at == None, Run.started_at != None, Run.started_at >= since)
                )
            )
            .group_by(Failure.cluster_id, "day")
            .all()
        )

        # Organize data by cluster
        cluster_data = defaultdict(list)
        for cluster_id, day, count in rows:
            cluster_data[cluster_id].append((day, count))

        # Process daily values
        for cluster_id, entries in cluster_data.items():
            entries.sort(key=lambda x: x[0])  # oldest first

            counts = [c for _, c in entries]

            for idx, (day, count) in enumerate(entries):

                # Moving averages
                last_7 = counts[max(0, idx - 6): idx + 1]
                last_30 = counts[max(0, idx - 29): idx + 1]

                avg7 = sum(last_7) / len(last_7)
                avg30 = sum(last_30) / len(last_30)

                # Trend direction
                if avg7 > avg30 * 1.2:
                    trend = 1.0  # rising
                elif avg7 < avg30 * 0.8:
                    trend = -1.0  # falling
                else:
                    trend = 0.0  # stable

                # Spike detection
                spike = 1 if (count > avg30 * 2.0 and count > 5) else 0

                # Upsert into DB
                row = db.query(ClusterTrend).filter(
                    ClusterTrend.cluster_id == cluster_id,
                    ClusterTrend.date == day
                ).first()

                if not row:
                    row = ClusterTrend(
                        cluster_id=cluster_id,
                        date=day,
                        failure_count=count,
                        moving_avg_7d=avg7,
                        moving_avg_30d=avg30,
                        trend_score=trend,
                        spike_flag=spike
                    )
                    db.add(row)
                else:
                    row.failure_count = count
                    row.moving_avg_7d = avg7
                    row.moving_avg_30d = avg30
                    row.trend_score = trend
                    row.spike_flag = spike

        db.commit()
