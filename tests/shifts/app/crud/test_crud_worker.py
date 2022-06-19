from datetime import date

from shifts.app.crud.crud_worker import CRUDWorker


def test_get_worker_by_username_calls_methods(db, model):
    # Set up
    username = "test"
    _model = model(username)
    crud = CRUDWorker(model=_model)

    # Exercise
    crud.get_worker_by_username(db, username=username)

    # Verify
    db.query.assert_called_with(_model)
    db.query().filter.assert_called_with(_model.username == username)
    db.query().filter().first.assert_called()


def test_get_worker_shift_by_date_calls_methods(db, model):
    # Set up
    worker_id = 1
    shift_date = date.today()
    _model = model()
    crud = CRUDWorker(model=_model)

    # Exercise
    crud.get_worker_shift_by_date(db, worker_id=worker_id, shift_date=shift_date)

    # Verify
    db.query.assert_called()
    db.query().join.assert_called()
    db.query().join().join.assert_called()
    db.query().join().join().filter.assert_called()
    db.query().join().join().filter().first.assert_called()
