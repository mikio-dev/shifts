# pylint: disable=E0611
from typing import Generator, Optional

from app.core.auth import oauth2_scheme
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm.session import Session


class TokenData(BaseModel):
    username: Optional[str] = None


def get_db() -> Generator:
    """
    The database session is injected as a dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as exc:
        raise credentials_exception from exc

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
