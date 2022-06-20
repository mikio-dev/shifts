from sqlalchemy.orm import relationship

from .user import User


class Worker(User):
    shifts = relationship(
        "WorkerShift",
        cascade="all, delete-orphan",
    )
    __mapper_args__ = {
        "polymorphic_identity": "worker",
    }
