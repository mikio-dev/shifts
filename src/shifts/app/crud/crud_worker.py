from datetime import date

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.models.shift import Shift
from app.models.worker import Worker
from app.models.worker_shift import WorkerShift
from app.schemas.worker import WorkerCreate
from sqlalchemy.orm import Session


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

    def get_shifts_by_worker(self, db: Session, worker_id: int):
        """
        Join worker, shift and worker_shift, select the records by worker_id,
        and returns all Shift records
        """
        return (
            db.query(Shift)
            .join(WorkerShift, WorkerShift.shift_id == Shift.id)
            .join(Worker, Worker.id == WorkerShift.worker_id)
            .filter(Worker.id == worker_id)
            .all()
        )

    def create(self, db: Session, *, obj_in: WorkerCreate):
        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj = self.model(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


worker = CRUDWorker(Worker)
