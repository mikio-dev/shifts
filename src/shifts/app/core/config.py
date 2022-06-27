# pylint: disable=E0611, E0213
import pathlib
from typing import Optional

from pydantic import BaseSettings

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # API versioning
    API_V1_STR: str = "/api/v1"

    # Database URI
    # SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///shifts.db"
    SQLALCHEMY_DATABASE_URI: Optional[
        str
    ] = "postgresql://postgres:postgres@localhost:5432/shifts"

    # Test data to be created in app/load_init_data.py
    FIRST_MANAGER: str = "Manager1"
    FIRST_MANAGER_PWD: str = "password123"
    FIRST_WORKER: str = "Worker1"
    FIRST_WORKER_PWD: str = "password123"

    # JWT secret
    JWT_SECRET: str = "TEST_JWT_SECRET"

    # JWT access token expiry time in minutes (defualt is 24 hours)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # JWS the signing algorithm (default is HS256)
    ALGORITHM: str = "HS256"

    class Config:
        case_sensitive = True


settings = Settings()
