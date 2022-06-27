from unittest.mock import MagicMock

import pytest
from app.schemas.user import User


@pytest.fixture
def db():
    mock = MagicMock()
    mock.query().filter().first.return_value = User(id=1, username="test")
    return mock


@pytest.fixture
def token():
    return MagicMock()
