from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.core.config import settings


def encode_jwt(
    payload: dict,
    secret_key: str = settings.jwt_secret,
    algorithm: str = settings.jwt_algorithm,
    expire_minutes: int = settings.jwt_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, key=secret_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str,
    secret_key: str = settings.jwt_secret,
    algorithm: str = settings.jwt_algorithm,
) -> dict:
    decoded = jwt.decode(jwt=token, key=secret_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    encoded: bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return encoded.decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )
