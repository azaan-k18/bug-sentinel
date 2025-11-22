"""
Seed dummy data for SentinelQA: websites, runs, failures, labels.

Run from backend root with venv active:
    cd backend
    source venv/bin/activate
    python -m app.scripts.seed_dummy_data
"""

import random
import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base

from app.models.website import Website
from app.models.run import Run
from app.models.failure import Failure
from app.models.label import Label

# ---------------------------------------------------------
# CONFIGURABLE SETTINGS
# ---------------------------------------------------------
NUM_WEBSITES = 4
RUNS_PER_SITE = 30
FAILURES_PER_RUN = (0, 4)  # (min, max)

SAMPLE_FAILURE_MESSAGES = [
    "AssertionError: expected 200 but got 500 at /articles/123",
    "TimeoutException: page did not load within 30s (Selector #main-article not found)",
    "NoSuchElementException: xpath=//button[@id='download'] not found",
    "ElementNotInteractableException: element is not interactable",
    "DatabaseError: could not connect to DB",
    "OSError: [Errno 13] Permission denied: '/tmp/cache'",
    "SslHandshakeException: SSL handshake failed",
    "AssertionError: text did not match expected snapshot",
    "TimeoutError: request timed out",
    "IndexError: list index out of range in ArticleParser"
]

LABEL_CLASSES = ["real_bug", "infra", "locator", "flaky", "test_issue", "other"]

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def create_tables():
    Base.metadata.create_all(bind=engine)

def random_timestamp(days_back=30):
    return datetime.utcnow() - timedelta(
        days=random.randint(0, days_back),
        seconds=random.randint(0, 60 * 60 * 24)
    )

# ---------------------------------------------------------
# MAIN SEED FUNCTION
# ---------------------------------------------------------
def seed():

    print("Creating tables (if missing)...")
    create_tables()

    db: Session = SessionLocal()

    try:
        print("Clearing existing data...")

        db.query(Label).delete()
        db.query(Failure).delete()
        db.query(Run).delete()
        db.query(Website).delete()
        db.commit()

        # -----------------------------------------
        # 1. CREATE WEBSITES
        # -----------------------------------------
        print("Seeding websites...")

        websites = []
        for i in range(1, NUM_WEBSITES + 1):
            w = Website(
                name=f"Site-{i}",
                domain=f"site{i}.example.com",
                description=f"Dummy site {i}"
            )
            db.add(w)
            websites.append(w)

        db.commit()

        # -----------------------------------------
        # 2. SEED RUNS + FAILURES
        # -----------------------------------------
        print("Seeding runs and failures...")

        for w in websites:

            for rnum in range(1, RUNS_PER_SITE + 1):

                started = random_timestamp(60)
                finished = started + timedelta(seconds=random.randint(20, 300))

                run = Run(
                    run_uid=str(uuid.uuid4()),
                    website_id=w.id,
                    jenkins_server=random.choice(["jenkins-1", "jenkins-2", "jenkins-3"]),
                    job_name=random.choice(["smoke", "regression", "epaper", "article-extract"]),
                    build_number=rnum,
                    status=random.choice(["SUCCESS", "FAIL"]),
                    started_at=started,
                    finished_at=finished,
                )

                db.add(run)
                db.flush()  # ensures run.id is available

                # Random # of failures
                count_failures = random.randint(*FAILURES_PER_RUN)

                for i in range(count_failures):

                    raw = random.choice(SAMPLE_FAILURE_MESSAGES)
                    extracted = raw.split(":")[0]  # simple extraction

                    failure = Failure(
                        run_id=run.id,
                        test_name=f"test_{i}",
                        platform=random.choice(["desktop", "mobile"]),
                        website=w.domain,
                        error_message=raw,
                        extracted_message=extracted,
                        website_id=w.id
                    )
                    db.add(failure)
                    db.flush()

                    # Attach a random label 60% of the time
                    if random.random() < 0.6:
                        lbl = Label(
                            failure_id=failure.id,
                            label=random.choice(LABEL_CLASSES),
                            confidence=round(random.uniform(0.50, 0.99), 2),
                            source=random.choice(["model", "human"]),
                            labeled_by=random.choice(["model_v1", "alice", "bob", None])
                        )
                        db.add(lbl)

        db.commit()

        print(f"\nSeed complete:")
        print(f"  Websites: {len(websites)}")
        print(f"  Runs per site: {RUNS_PER_SITE}")
        print(f"  Total runs: {NUM_WEBSITES * RUNS_PER_SITE}")
        print("  Failures and labels added as random simulations.\n")

    finally:
        db.close()


# ---------------------------------------------------------
# EXECUTE WHEN RUN DIRECTLY
# ---------------------------------------------------------
if __name__ == "__main__":
    seed()
