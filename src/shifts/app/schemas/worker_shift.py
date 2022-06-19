# pylint: disable=E0611
from datetime import date

from pydantic import BaseModel


class WorkerShiftBase(BaseModel):
    worker_id: int
    shift_id: int
    shift_date: date

    class Config:
        orm_mode = True


class WorkerShiftCreate(WorkerShiftBase):
    pass


class WorkerShiftUpdate(WorkerShiftBase):
    pass


class UserInDBBase(WorkerShiftBase):
    pass


class WorkerShift(UserInDBBase):
    pass
