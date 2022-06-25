from app.db.base_class import Base
from sqlalchemy import DATE, Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    shift_date = Column(DATE, index=True)
    shift_slot = Column(Integer, index=True)
    workers = relationship(
        "WorkerShift",
        cascade="all, delete-orphan",
    )
    __table_args__ = (
        UniqueConstraint("shift_date", "shift_slot", name="shift_date_shift_slot_uc"),
    )
