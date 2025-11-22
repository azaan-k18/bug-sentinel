from sqlalchemy import Column, Integer, Text
from app.db.base import Base

class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    domain = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
