from sqlalchemy.orm import Session

from shifts.app.crud.base import CRUDBase
from shifts.app.models.manager import Manager
from shifts.app.schemas.manager import ManagerCreate


class CRUDManager(CRUDBase[Manager, ManagerCreate]):
    def get_manager_by_username(self, db: Session, *, username: str):
        """
        Select manager records by the username and returns the first record
        """
        return db.query(self.model).filter(self.model.username == username).first()


manager = CRUDManager(Manager)
