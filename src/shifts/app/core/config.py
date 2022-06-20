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
    FIRST_WORKER: str = "Worker1"

    class Config:
        case_sensitive = True


settings = Settings()
