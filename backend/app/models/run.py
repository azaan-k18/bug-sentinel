from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base

class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)

    # Unique ID coming from Jenkins or your system
    run_uid = Column(Text, index=True, nullable=False)

    # Optional relational website ID (we'll integrate website later)
    website_id = Column(Integer, nullable=True)

    jenkins_server = Column(Text, nullable=True)
    job_name = Column(Text, nullable=True)
    build_number = Column(Integer, nullable=True)
    status = Column(Text, nullable=True)

    started_at = Column(TIMESTAMP, nullable=True)
    finished_at = Column(TIMESTAMP, nullable=True)

    raw_log_path = Column(Text, nullable=True)

    failures = relationship("Failure", back_populates="run", cascade="all, delete-orphan")
