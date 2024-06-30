from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get a password hash."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """Creates an access token."""
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(
        to_encode,
        settings.SECURITY.SECRET_KEY,
        algorithm=settings.SECURITY.ALGORITHM,
    )
