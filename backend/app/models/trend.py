from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class ClusterTrend(Base):
    __tablename__ = "cluster_trends"

    id = Column(Integer, primary_key=True, index=True)

    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=False)
    date = Column(Date, nullable=False)

    failure_count = Column(Integer, nullable=False, default=0)
    moving_avg_7d = Column(Float, nullable=True)
    moving_avg_30d = Column(Float, nullable=True)

    trend_score = Column(Float, nullable=True)  # +1 rising, -1 falling, 0 stable
    spike_flag = Column(Integer, default=0)     # 1 = spike, 0 = normal

    cluster = relationship("Cluster")
