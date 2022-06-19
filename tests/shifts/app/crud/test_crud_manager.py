from shifts.app.crud.crud_manager import CRUDManager


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
