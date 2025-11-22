# app/models/cluster.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.dialects.postgresql import JSONB

class Cluster(Base):
    __tablename__ = "clusters"
    id = Column(Integer, primary_key=True, index=True)
    representative_message = Column(Text, nullable=True)
    # JSON encoded embedding (list of floats) - if Postgres you can use JSONB; here we keep Text for portability
    representative_embedding = Column(Text, nullable=True)
    member_count = Column(Integer, default=0, nullable=False)
    cluster_metadata = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())