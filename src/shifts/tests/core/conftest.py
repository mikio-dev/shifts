from unittest.mock import MagicMock

import pytest
from app.core.security import get_password_hash
from app.models.user import User


@pytest.fixture
def db():
    def _db(username: str, password: str):
        d = MagicMock()
        hashed_password = get_password_hash(password)
        d.query().filter().first.return_value = User(
            username=username, hashed_password=hashed_password
        )
        return d

    return _db
