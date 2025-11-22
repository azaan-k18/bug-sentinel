from pydantic import BaseSettings, AnyHttpUrl
from typing import List, Optional

class Settings(BaseSettings):
    # DB (example: postgresql://user:pass@localhost:5432/dbname)
    DATABASE_URL: str = "postgresql://sentinel:sentinel@localhost:5432/sentinelqa"
    # optional sqlite fallback for dev local runs
    SQLITE_URL: str = "sqlite:///./dev.db"
    BACKEND_CORS_ORIGINS: Optional[List[AnyHttpUrl]] = None

    # ML model path
    MODEL_PATH: str = "./ml/models/current"

    # Security
    JWT_SECRET: str = "change-me-in-prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
