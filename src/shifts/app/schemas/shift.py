# pylint: disable=E0611
from datetime import date
from typing import Optional

from pydantic import BaseModel

from .worker_shift import WorkerShift


class ShiftBase(BaseModel):
    shift_date: date
    shift_slot: int
    num_workers: int


class ShiftCreate(ShiftBase):
    pass


class ShiftUpdate(ShiftBase):
    pass


class ShiftInDBBase(ShiftBase):
    id: Optional[int] = None
    workers: list[WorkerShift] = []

    class Config:
        orm_mode = True


class Shift(ShiftInDBBase):
    pass
