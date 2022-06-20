from sqlalchemy import DATE, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from app.db.base_class import Base


class WorkerShift(Base):
    __tablename__ = "worker_shift"
    worker_id = Column(ForeignKey("users.id"), primary_key=True)
    shift_id = Column(ForeignKey("shifts.id"), primary_key=True)
    shift_date = Column(DATE)
    worker = relationship(
        "Worker",
        back_populates="shifts",
    )
    shift = relationship(
        "Shift",
        back_populates="workers",
    )
    __table_args__ = (
        UniqueConstraint("worker_id", "shift_date", name="worker_id_shift_date_uc"),
    )
