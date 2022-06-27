from app import crud
from app.api import deps
from app.schemas.shift import Shift
from app.schemas.user import User
from app.schemas.worker import Worker, WorkerCreate
from app.schemas.worker_shift import WorkerShift
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .shift import fetch_shift

router = APIRouter()


@router.get("/", status_code=200, response_model=list[Worker])
def search_workers(
    *, skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)
):
    """
    Return all workers
    """
    workers = crud.worker.get_multi(db, skip=skip, limit=limit)
    return workers


@router.get("/{worker_id}", status_code=200, response_model=Worker)
def fetch_worker(*, worker_id: int, db: Session = Depends(deps.get_db)):
    """
    Fetch a single worker by ID
    """
    db_worker = crud.worker.get(db, id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


@router.post("/", status_code=201, response_model=Worker)
def create_worker(
    *,
    worker: WorkerCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new worker
    """
    if current_user.type != "manager":
        raise HTTPException(status_code=401, detail="Not authorized")

    db_worker = crud.worker.get_worker_by_username(db, username=worker.username)
    if db_worker:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.worker.create(db=db, obj_in=worker)


@router.delete("/{worker_id}", status_code=200)
def delete_worker(
    *,
    worker_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete a worker
    """
    if current_user.type != "manager":
        raise HTTPException(status_code=401, detail="Not authorized")

    crud.worker.remove(db=db, id=worker_id)
    return worker_id


@router.get("/{worker_id}/shifts/", status_code=200, response_model=list[Shift])
def get_my_shifts(
    *,
    worker_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Fetch all shifts for the specified worker
    """
    return crud.worker.get_shifts_by_worker(db, worker_id)


@router.post(
    "/{worker_id}/shifts/{shift_id}",
    status_code=200,
    response_model=WorkerShift,
)
def add_shift_to_worker(
    worker_id: int,
    shift_id: int,
    db: Session = Depends(deps.get_db),
    current_worker: Worker = Depends(deps.get_current_user),
):
    """
    Add shift to worker
    """
    if worker_id != current_worker.id:
        raise HTTPException(status_code=401, detail="Not authorized")

    fetch_worker(worker_id=worker_id, db=db)
    db_shift = fetch_shift(shift_id=shift_id, db=db)
    db_worker_shift = crud.worker.get_worker_shift_by_date(
        db, worker_id=worker_id, shift_date=db_shift.shift_date
    )
    if db_worker_shift is not None:
        # The worker already has a shift on the same day
        # So, return a 409 error
        raise HTTPException(
            status_code=409,
            detail=(
                "Worker already has a Shift on the specified date."
                f"{jsonable_encoder(db_worker_shift)}"
            ),
        )

    try:
        db_worker_shift = crud.worker_shift.add_shift_to_worker(
            db, worker_id, shift_id, db_shift.shift_date
        )
    except IntegrityError as exc:
        # There are two unique constraints in the database
        # - PK: (worker_id, shift_id)
        # - Unique: (worker_id, shift_date)
        raise HTTPException(
            status_code=409,
            detail="Worker already has the Shift.",
        ) from exc

    return db_worker_shift


@router.delete(
    "/{worker_id}/shifts/{shift_id}",
    status_code=200,
    response_model=WorkerShift,
)
def delete_shift_from_worker(
    worker_id: int,
    shift_id: int,
    db: Session = Depends(deps.get_db),
    current_worker: Worker = Depends(deps.get_current_user),
):
    """
    Delete shift from worker
    """
    if worker_id != current_worker.id:
        raise HTTPException(status_code=401, detail="Not authorized")

    fetch_worker(worker_id=worker_id, db=db)
    fetch_shift(shift_id=shift_id, db=db)
    db_worker_shift = crud.worker_shift.get_worker_shift_by_id(
        db, worker_id=worker_id, shift_id=shift_id
    )
    if db_worker_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return crud.worker_shift.remove_worker_shift(
        db=db, worker_id=worker_id, shift_id=shift_id
    )
