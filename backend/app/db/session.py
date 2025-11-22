from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# prefer DATABASE_URL but allow sqlite fallback if you want to run without Postgres
DATABASE_URL = settings.DATABASE_URL or settings.SQLITE_URL

# SQLAlchemy engine & session
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
