from datetime import date

from shifts.app.crud.crud_worker_shift import CRUDWorkerShift


def test_get_worker_shift_by_id_calls_methods(db, model):
    # Set up
    worker_id = 1
    shift_id = 2
    _model = model(worker_id=worker_id, shift_id=shift_id)
    crud = CRUDWorkerShift(model=_model)

    # Exercise
    crud.get_worker_shift_by_id(db, worker_id=worker_id, shift_id=shift_id)

    # Verify
    db.query.assert_called_with(_model)
    db.query().filter.assert_called_with(
        _model.worker_id == worker_id, _model.shift_id == shift_id
    )
    db.query().filter().first.assert_called()


def test_add_shift_to_worker_calls_methods(db, model):
    # Set up
    worker_id = 1
    shift_id = 2
    shift_date = date.today()
    _model = model()
    crud = CRUDWorkerShift(model=_model)

    # Exercise
    crud.add_shift_to_worker(
        db, worker_id=worker_id, shift_id=shift_id, shift_date=shift_date
    )

    # Verify
    crud.model.assert_called_with(
        worker_id=worker_id, shift_id=shift_id, shift_date=shift_date
    )
    db.add.assert_called()
    db.commit.assert_called()
    db.refresh.assert_called()


def test_remove_calls_methods(db, model):
    # Set up
    worker_id = 1
    shift_id = 2
    _model = model(worker_id=worker_id, shift_id=shift_id)
    crud = CRUDWorkerShift(model=_model)

    # Exercise
    crud.remove_worker_shift(db, worker_id=worker_id, shift_id=shift_id)

    # Verify
    db.query.assert_called_with(_model)
    db.delete.assert_called()
    db.commit.assert_called()
