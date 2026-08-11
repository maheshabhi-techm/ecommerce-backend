from jose import jwt
from datetime import datetime, timedelta
from src.security.config import settings


def create_access_token(user):
    expire = datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user.id),
        "role": user.role.value,
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(user_id: int):
    expire = datetime.now() + timedelta(days=7)

    payload = {"sub": user_id, "exp": expire, "type": "refresh"}

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
