# pylint: disable=E0611
from typing import Generator

from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    The database session is injected as a dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
