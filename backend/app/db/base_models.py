# Import Base
from app.db.base import Base

# Import all your SQLAlchemy models here
# This file exists ONLY to load model metadata for Alembic
from app.models.run import Run
from app.models.failure import Failure
from app.models.label import Label
from app.models.cluster import Cluster
from app.models.website import Website
from app.models.flakiness import Flakiness