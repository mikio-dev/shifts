from datetime import date

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.shift import Shift
from app.schemas.shift import ShiftCreate


class CRUDShift(CRUDBase[Shift, ShiftCreate]):
    def get_shift_by_date_slot(self, db: Session, shift_date: date, shift_slot: int):
        """
        Select shift records and returns the first record
        """
        return (
            db.query(self.model)
            .filter(
                self.model.shift_date == shift_date,
                self.model.shift_slot == shift_slot,
            )
            .first()
        )


shift = CRUDShift(Shift)
