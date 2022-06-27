from .user import UserBase, UserCreate, UserInDBBase
from .worker_shift import WorkerShift


class WorkerBase(UserBase):
    pass


class WorkerCreate(UserCreate):
    pass


class WorkerUpdate(UserCreate):
    pass


class WorkerInDBBase(UserInDBBase):
    shifts: list[WorkerShift] = []

    class Config:
        orm_mode = True


class WorkerInDB(WorkerInDBBase):
    hashed_password: str


class Worker(WorkerInDBBase):
    pass
