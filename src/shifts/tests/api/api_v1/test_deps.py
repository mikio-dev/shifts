from unittest.mock import MagicMock

import app
import pytest
from app.api.deps import get_current_user, get_db
from app.schemas.user import User
from jose import JWTError
from sqlalchemy.orm import Session


def test_get_db():

    # get_db() returns a Session object as a Generator object

    # Set up

    # Exercise
    db = get_db()

    # Verify
    assert db is not None
    assert isinstance(next(db), Session)
    db.close()


@pytest.mark.asyncio
async def test_get_current_user_returns_user(db, token):

    # Set up
    app.api.deps.jwt = MagicMock()
    app.api.deps.jwt.decode.return_value = {"sub": "test"}

    # Exercise
    user = await get_current_user(db, token)

    # Verify
    assert user is not None
    assert isinstance(user, User)


@pytest.mark.asyncio
async def test_get_current_user_raises_unauthorized(db, token):

    # Set up
    app.api.deps.jwt = MagicMock()
    app.api.deps.jwt.decode.return_value = {"sub": None}

    # Exercise
    with pytest.raises(Exception) as exc:
        await get_current_user(db, token)

    # Verify
    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"
    assert exc.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.mark.asyncio
async def test_get_current_user_raises_jwterror(db, token):

    # Set up
    app.api.deps.jwt = MagicMock()
    app.api.deps.jwt.decode.side_effect = JWTError()

    # Exercise
    with pytest.raises(Exception) as exc:
        await get_current_user(db, token)

    # Verify
    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"
    assert exc.value.headers == {"WWW-Authenticate": "Bearer"}
