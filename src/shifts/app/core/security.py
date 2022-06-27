from passlib.context import CryptContext

ctx = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return ctx.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return ctx.hash(password)
