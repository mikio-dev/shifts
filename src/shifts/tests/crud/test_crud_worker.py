from datetime import date
from unittest.mock import MagicMock

from app.crud.crud_worker import CRUDWorker


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


def test_get_shifts_by_worker_calls_methods(db, model):
    # Set up
    worker_id = 1
    _model = model()
    crud = CRUDWorker(model=_model)

    # Exercise
    crud.get_shifts_by_worker(db, worker_id=worker_id)

    # Verify
    db.query.assert_called()
    db.query().join.assert_called()
    db.query().join().join.assert_called()
    db.query().join().join().filter.assert_called()
    db.query().join().join().filter().all.assert_called()


def test_remove_calls_methods(db, model):
    # Set up
    worker_id = 1
    _model = model()
    crud = CRUDWorker(model=_model)

    # Exercise
    crud.remove(db, id=worker_id)

    # Verify
    db.query.assert_called_with(_model)
    db.query(_model).get.assert_called_with(worker_id)
    db.delete.assert_called()
    db.commit.assert_called()


def test_create_calls_methods(db, model):
    # Set up
    dict_no_password = {"key": "value"}
    password = "password123"
    obj_in = MagicMock()
    obj_in.password = password
    obj_in.dict.return_value = {**dict_no_password, "password": password}
    _model = model(_id=1)
    crud = CRUDWorker(model=_model)

    # Exercise
    crud.create(db, obj_in=obj_in)

    # Verify
    crud.model.assert_called_with(**dict_no_password)
    db.add.assert_called()
    db.commit.assert_called()
    db.refresh.assert_called()
