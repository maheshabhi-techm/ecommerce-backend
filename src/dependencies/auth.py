from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import Depends
from src.security.config import settings
from fastapi import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )

        return {"user_id": int(payload["sub"]), "role": payload["role"]}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
