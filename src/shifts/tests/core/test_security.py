from app.core.security import get_password_hash, verify_password


def test_password_hash():
    password = "password123"
    hashed_password = get_password_hash(password)

    assert len(hashed_password) > 0
    assert hashed_password != password
    assert verify_password(password, hashed_password)
