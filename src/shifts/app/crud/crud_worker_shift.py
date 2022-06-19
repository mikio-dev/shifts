from datetime import date

from sqlalchemy.orm import Session

from shifts.app.crud.base import CRUDBase
from shifts.app.models.worker_shift import WorkerShift
from shifts.app.schemas.worker_shift import WorkerShiftCreate


class CRUDWorkerShift(CRUDBase[WorkerShift, WorkerShiftCreate]):
    def get_worker_shift_by_id(self, db: Session, worker_id: int, shift_id: int):
        """
        Select a single record by ID
        """
        return (
            db.query(self.model)
            .filter(self.model.worker_id == worker_id, self.model.shift_id == shift_id)
            .first()
        )

    def add_shift_to_worker(
        self, db: Session, worker_id: int, shift_id: int, shift_date: date
    ):
        """
        Create a new worker_shift record and insert into into the table
        """
        db_worker_shift = self.model(
            worker_id=worker_id, shift_id=shift_id, shift_date=shift_date
        )
        db.add(db_worker_shift)
        db.commit()
        db.refresh(db_worker_shift)
        return db_worker_shift

    def remove_worker_shift(self, db: Session, *, worker_id: int, shift_id: int):
        """
        Delete the specified record by IDs
        """
        obj = self.get_worker_shift_by_id(db, worker_id=worker_id, shift_id=shift_id)
        db.delete(obj)
        db.commit()
        return obj


worker_shift = CRUDWorkerShift(WorkerShift)
