from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Failure(Base):
    __tablename__ = "failures"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False)

    test_name = Column(Text, nullable=False)
    platform = Column(Text, nullable=False)
    website = Column(Text, nullable=False)
    error_message = Column(Text, nullable=True)
    extracted_message = Column(Text, nullable=True)
    website_id = Column(Integer, nullable=True)

    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=True, index=True)
    embedding = Column(Text, nullable=True) #this is JSON encoded embedding list

    run = relationship("Run", back_populates="failures")
    labels = relationship("Label", back_populates="failure", cascade="all, delete-orphan")
    cluster = relationship("Cluster", backref="failures")
