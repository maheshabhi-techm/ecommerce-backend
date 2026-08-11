from fastapi.params import Depends
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone, UTC
from fastapi.security import OAuth2PasswordBearer
import jwt
from .config import settings

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        # return {
        #     "user_id": payload[sub],
        #     "role": payload[role]
        # }
        return payload
    except jwt.PyJWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        user_id = payload.get("user_id")
    except jwt.PyJWTError:
        return None


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire})

    encode_jwt_refresh = jwt.encode(to_encode, settings.secret_key, settings.algorithm)

    return encode_jwt_refresh
