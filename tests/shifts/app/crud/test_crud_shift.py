from datetime import date

from shifts.app.crud.crud_shift import CRUDShift


def test_get_shift_by_date_slot(db, model):
    # Set up
    shift_date = date.today()
    shift_slot = 1
    _model = model(shift_date=shift_date, shift_slot=shift_slot)
    crud = CRUDShift(model=_model)

    # Exercise
    crud.get_shift_by_date_slot(db, shift_date=shift_date, shift_slot=shift_slot)

    # Verify
    db.query.assert_called_with(_model)
    db.query().filter.assert_called_with(
        _model.shift_date == shift_date, _model.shift_slot == shift_slot
    )
    db.query().filter().first.assert_called()
