from sqlalchemy import DATE, Column, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    shift_date = Column(DATE, index=True)
    shift_slot = Column(Integer, index=True)
    workers = relationship(
        "WorkerShift",
        cascade="all, delete-orphan",
    )