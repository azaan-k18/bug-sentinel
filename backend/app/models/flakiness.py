from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.db.base import Base

class Flakiness(Base):
    __tablename__ = "flakiness"

    id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String, index=True, nullable=False)
    job_name = Column(String, index=True, nullable=True)

    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)

    flakiness_score = Column(Float, default=0.0)

    last_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )