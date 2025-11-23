from app.db.session import SessionLocal
import app.db.base_models

from app.ml.trend_engine import TrendEngine

def run_backfill():
    db = SessionLocal()

    engine = TrendEngine(days=180)
    engine.compute_daily_trends(db)

    print("Cluster trends backfilled.")

    db.close()

if __name__ == "__main__":
    run_backfill()