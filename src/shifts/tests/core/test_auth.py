import pytest

from datetime import datetime, timedelta
from jose import jwt

from app.core.auth import authenticate, create_access_token
from app.core.config import settings


def test_authenticate_returns_correct_user(db):
    username = "test"
    password = "password123"
    returned_user = authenticate(
        username=username, password=password, db=db(username, password)
    )

    assert username == returned_user.username


@pytest.mark.parametrize("user_id", [str(1), 1, None, ""])
def test_create_access_token_returns_token(user_id):
    cur_time = datetime.now()
    lifetime = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(sub=user_id)

    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.ALGORITHM],
        options={"verify_aud": False},
    )

    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access_token"

    # The expiry timestamp should be within a few seconds of the current time plus the lifetime
    assert (
        payload["exp"] >= int((cur_time + lifetime).timestamp())
        and payload["exp"] < int((cur_time + lifetime).timestamp()) + 3
    )
