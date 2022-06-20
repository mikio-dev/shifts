# pylint: disable=E0611
from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from .worker_shift import WorkerShift


class ShiftSlot(int, Enum):
    slot_00_08 = 1
    slot_08_16 = 2
    slot_16_24 = 3


class ShiftBase(BaseModel):
    shift_date: date
    shift_slot: ShiftSlot


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
