from sqlalchemy import Column, Integer, Text, Float, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    failure_id = Column(Integer, ForeignKey("failures.id"), nullable=False)
    label = Column(Text, nullable=False)
    confidence = Column(Float, nullable=True)
    source = Column(Text, default="model")
    labeled_by = Column(Text, nullable=True)
    labeled_at = Column(TIMESTAMP, server_default=func.now())
