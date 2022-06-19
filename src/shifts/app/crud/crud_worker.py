from datetime import date

from sqlalchemy.orm import Session

from shifts.app.crud.base import CRUDBase
from shifts.app.models.shift import Shift
from shifts.app.models.worker import Worker
from shifts.app.models.worker_shift import WorkerShift
from shifts.app.schemas.worker import WorkerCreate


class CRUDWorker(CRUDBase[Worker, WorkerCreate]):
    def get_worker_by_username(self, db: Session, *, username: str):
        """
        Select worker records by username and returns the first record
        """
        return db.query(self.model).filter(self.model.username == username).first()

    def get_worker_shift_by_date(self, db: Session, worker_id: int, shift_date: date):
        """
        Join worker, shift and worker_shift, select the records by worker_id and shift_date,
        and returns the first record
        """
        return (
            db.query(
                Worker.id.label("worker_id"),
                Shift.shift_date,
                Shift.shift_slot,
            )
            .join(WorkerShift, Worker.id == WorkerShift.worker_id)
            .join(Shift, Shift.id == WorkerShift.shift_id)
            .filter(Worker.id == worker_id, Shift.shift_date == shift_date)
            .first()
        )


worker = CRUDWorker(Worker)
