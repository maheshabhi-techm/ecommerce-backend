from fastapi import Depends, HTTPException
from src.dependencies.auth import get_current_user


def require_roles(*allowed_roles):
    def dependency(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Permission denied")

        return user

    return dependency
