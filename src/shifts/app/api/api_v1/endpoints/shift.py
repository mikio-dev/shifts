# pylint: disable=E1101
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from shifts.app import crud
from shifts.app.api import deps
from shifts.app.schemas.shift import Shift, ShiftCreate

router = APIRouter()


@router.get("/", status_code=200, response_model=list[Shift])
def search_shifts(
    *, skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)
):
    """
    Return all shifts
    """
    shifts = crud.shift.get_multi(db, skip=skip, limit=limit)
    return shifts


@router.get("/{shift_id}", status_code=200, response_model=Shift)
def fetch_shift(*, shift_id: int, db: Session = Depends(deps.get_db)):
    """
    Fetch a single shift by ID
    """
    db_shift = crud.shift.get(db, id=shift_id)
    if db_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return db_shift


@router.post("/", status_code=201, response_model=Shift)
def create_shift(*, shift: ShiftCreate, db: Session = Depends(deps.get_db)):
    """
    Create a new shift
    """
    db_shift = crud.shift.get_shift_by_date_slot(
        db, shift_date=shift.shift_date, shift_slot=shift.shift_slot
    )
    if db_shift:
        raise HTTPException(status_code=400, detail="Shift already exists")
    return crud.shift.create(db=db, obj_in=shift)


@router.delete("/{shift_id}", status_code=200)
def delete_shift(*, shift_id: int, db: Session = Depends(deps.get_db)):
    """
    Delete a shift
    """
    fetch_shift(shift_id=shift_id, db=db)
    return crud.shift.remove(db=db, id=shift_id)
