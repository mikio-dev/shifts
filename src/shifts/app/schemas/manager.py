from .user import UserBase, UserCreate, UserInDBBase


class ManagerBase(UserBase):
    pass


class ManagerCreate(UserCreate):
    pass


class ManagerUpdate(UserCreate):
    pass


class ManagerInDBBase(UserInDBBase):
    class Config:
        orm_mode = True


class Manager(ManagerInDBBase):
    pass
