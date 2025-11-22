from app.db.session import SessionLocal
import app.db.base_models

from app.ml.flakiness import FlakinessEngine

def run_backfill():
    db = SessionLocal()
    engine = FlakinessEngine(window_days=180)  # longer history for initial backfill

    records = engine.calculate_flakiness(db)

    print("Flakiness backfilled for", len(records), "tests")
    for r in records:
        print(r)

    db.close()


if __name__ == "__main__":
    run_backfill()
