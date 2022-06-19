from datetime import date
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def model():
    def _model(
        _id: int = None,
        username: str = None,
        shift_date: date = None,
        shift_slot: int = None,
        worker_id: int = None,
        shift_id: int = None,
    ):
        m = MagicMock()
        m.id = _id
        m.username = username
        m.shift_date = shift_date
        m.shift_slot = shift_slot
        m.worker_id = worker_id
        m.shift_id = shift_id
        m.dict = lambda: {"key": "value"}

        return m

    return _model


@pytest.fixture
def db():
    d = MagicMock()
    return d
