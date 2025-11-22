from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Failure(Base):
    __tablename__ = "failures"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False)
    website_id = Column(Integer, nullable=True)  # optional denormalized field
    error_message = Column(Text, nullable=True)
    extracted_message = Column(Text, nullable=True)

    run = relationship("Run", back_populates="failures")
