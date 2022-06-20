# pylint: disable=E1101
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.manager import Manager, ManagerCreate

router = APIRouter()


@router.get("/", status_code=200, response_model=list[Manager])
def search_managers(
    *, skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)
):
    """
    Return all managers
    """
    managers = crud.manager.get_multi(db, skip=skip, limit=limit)
    return managers


@router.get("/{manager_id}", status_code=200, response_model=Manager)
def fetch_manager(*, manager_id: int, db: Session = Depends(deps.get_db)):
    """
    Fetch a single manager by ID
    """
    db_manager = crud.manager.get(db, id=manager_id)
    if db_manager is None:
        raise HTTPException(status_code=404, detail="Manager not found")
    return db_manager


@router.post("/", status_code=201, response_model=Manager)
def create_manager(*, manager: ManagerCreate, db: Session = Depends(deps.get_db)):
    """
    Create a new manager
    """
    db_manager = crud.manager.get_manager_by_username(db, username=manager.username)
    if db_manager:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.manager.create(db=db, obj_in=manager)


@router.delete("/{manager_id}", status_code=200)
def delete_manager(*, manager_id: int, db: Session = Depends(deps.get_db)):
    """
    Delete a manager
    """
    fetch_manager(manager_id=manager_id, db=db)
    return crud.manager.remove(db=db, id=manager_id)
