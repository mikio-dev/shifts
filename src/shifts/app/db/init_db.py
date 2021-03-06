# pylint: disable=E1101, W1203
import datetime
import logging

from app import crud, schemas
from app.core.config import settings
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:

    if settings.FIRST_WORKER:
        worker = crud.worker.get_worker_by_username(db, username=settings.FIRST_WORKER)
        if not worker:
            worker_in = schemas.WorkerCreate(
                username=settings.FIRST_WORKER, password=settings.FIRST_WORKER_PWD
            )
            worker = crud.worker.create(db, obj_in=worker_in)
        else:
            logger.warning(
                "Skipping creating worker. Worker with username "
                f"{settings.FIRST_WORKER} already exists. "
            )

    if settings.FIRST_MANAGER:
        manager = crud.manager.get_manager_by_username(
            db, username=settings.FIRST_MANAGER
        )
        if not manager:
            manager_in = schemas.ManagerCreate(
                username=settings.FIRST_MANAGER, password=settings.FIRST_MANAGER_PWD
            )
            manager = crud.manager.create(db, obj_in=manager_in)
        else:
            logger.warning(
                "Skipping creating manager. Manager with username "
                f"{settings.FIRST_MANAGER} already exists. "
            )

        # Create initial shifts for the next 7 days
        shift_date = datetime.date.today()
        for _ in range(7):
            for shift_slot in range(1, 4):
                shift = crud.shift.get_shift_by_date_slot(
                    db, shift_date=shift_date, shift_slot=shift_slot
                )

                if not shift:
                    shift_in = schemas.ShiftCreate(
                        shift_date=shift_date,
                        shift_slot=shift_slot,
                    )
                    crud.shift.create(db, obj_in=shift_in)
            shift_date += datetime.timedelta(days=1)

        # Create initial worker_shift
        shift_date = datetime.date.today()
        worker = crud.worker.get_worker_by_username(db, username=settings.FIRST_WORKER)
        shift = crud.shift.get_shift_by_date_slot(
            db, shift_date=shift_date, shift_slot=1
        )

        worker_shift = crud.worker_shift.get_worker_shift_by_id(
            db, worker_id=worker.id, shift_id=shift.id
        )
        if not worker_shift:
            crud.worker_shift.add_shift_to_worker(
                db, worker_id=worker.id, shift_id=shift.id, shift_date=shift_date
            )
