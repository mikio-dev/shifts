from app.crud.base import CRUDBase
from app.models.manager import Manager
from app.schemas.manager import ManagerCreate
from sqlalchemy.orm import Session

from app.core.security import get_password_hash


class CRUDManager(CRUDBase[Manager, ManagerCreate]):
    def get_manager_by_username(self, db: Session, *, username: str):
        """
        Select manager records by the username and returns the first record
        """
        return db.query(self.model).filter(self.model.username == username).first()

    def create(self, db: Session, *, obj_in: ManagerCreate):
        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj = self.model(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


manager = CRUDManager(Manager)
