from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.ingestion import router as ingestion_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.failures import router as failures_router
from app.api.v1.auth import router as auth_router
from app.api.v1.review import router as review_router

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

CREATE_TABLES_ON_STARTUP = False  # set True when DB is up & you want tables created automatically

app = FastAPI(title="SentinelQA Analytics API", version="1.0.0")

# CORS (adjust origins for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS or ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(ingestion_router, prefix="/api/v1/ingest", tags=["ingest"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(failures_router, prefix="/api/v1/failures", tags=["failures"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(review_router, prefix="/api/v1/review", tags=["review"])

@app.on_event("startup")
def startup_event():
    if CREATE_TABLES_ON_STARTUP:
        # create DB tables (only do this for dev or first-run)
        Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "SentinelQA Backend"}