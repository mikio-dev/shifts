from unittest.mock import MagicMock

from app.crud.crud_manager import CRUDManager


def test_get_manager_by_username_calls_methods(db, model):
    # Set up
    username = "test"
    _model = model(username)
    crud = CRUDManager(model=_model)

    # Exercise
    crud.get_manager_by_username(db, username=username)

    # Verify
    db.query.assert_called_with(_model)
    db.query().filter.assert_called_with(_model.username == username)
    db.query().filter().first.assert_called()


def test_create_calls_methods(db, model):
    # Set up
    dict_no_password = {"key": "value"}
    password = "password123"
    obj_in = MagicMock()
    obj_in.password = password
    obj_in.dict.return_value = {**dict_no_password, "password": password}
    _model = model(_id=1)
    crud = CRUDManager(model=_model)

    # Exercise
    crud.create(db, obj_in=obj_in)

    # Verify
    crud.model.assert_called_with(**dict_no_password)
    db.add.assert_called()
    db.commit.assert_called()
    db.refresh.assert_called()
