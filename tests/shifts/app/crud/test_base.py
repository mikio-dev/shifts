import pytest

from shifts.app.crud.base import CRUDBase
from shifts.app.crud.crud_manager import CRUDManager
from shifts.app.crud.crud_shift import CRUDShift
from shifts.app.crud.crud_worker import CRUDWorker


@pytest.mark.parametrize("CLS", [CRUDBase, CRUDManager, CRUDShift, CRUDWorker])
class TestCRUDBase:
    def test_init_sets_property(self, CLS, model):
        # Set up
        _model = model(1)

        # Exercise
        crud = CLS(model=_model)

        # Verify
        assert crud.model == _model

    def test_get_calls_methods(self, CLS, model, db):
        # Set up
        _id = 1
        _model = model(_id=_id)
        crud = CLS(model=_model)

        # Exercise
        crud.get(db, _id)

        # Verify
        db.query.assert_called_with(_model)
        db.query().filter.assert_called_with(_model.id == _id)
        db.query().filter().first.assert_called()

    def test_get_multi_calls_methods(self, CLS, model, db):
        # Set up
        skip = 1
        limit = 2
        _model = model(_id=1)
        crud = CLS(model=_model)

        # Exercise
        crud.get_multi(db, skip=skip, limit=limit)

        # Verify
        db.query.assert_called_with(_model)
        db.query().offset.assert_called_with(skip)
        db.query().offset(skip).limit.assert_called_with(limit)
        db.query().offset(skip).limit(limit).all.assert_called()

    def test_create_calls_methods(self, CLS, model, db):
        # Set up
        obj_in = {"key": "value"}
        _model = model(_id=1)
        crud = CLS(model=_model)

        # Exercise
        crud.create(db, obj_in=obj_in)

        # Verify
        crud.model.assert_called_with(**obj_in)
        db.add.assert_called()
        db.commit.assert_called()
        db.refresh.assert_called()

    def test_remove_calls_methods(self, CLS, model, db):
        # Set up
        _id = 1
        _model = model(_id=_id)
        crud = CLS(model=_model)

        # Exercise
        crud.remove(db, id=_id)

        # Verify
        db.query.assert_called_with(_model)
        db.query(_model).get.assert_called_with(_id)
        db.delete.assert_called()
        db.commit.assert_called()
