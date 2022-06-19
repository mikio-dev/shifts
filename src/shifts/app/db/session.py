from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shifts.app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    # required for sqlite
    connect_args={"check_same_thread": False},
    # For the debugging purposes
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
