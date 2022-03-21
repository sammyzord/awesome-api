from typing import Dict, Any, Generator
from fastapi import Depends, HTTPException
from .db import get_db
from ..services.user import UserDBService
from .auth import validate_jwt


def get_user_service() -> Generator[UserDBService, None, None]:
    db = get_db()
    try:
        yield UserDBService(db)
    finally:
        db.close()


def get_current_user(
    jwt_payload: Dict[str, Any] = Depends(validate_jwt),
    user_service: UserDBService = Depends(get_user_service),
):
    user, err = user_service.auth_user(jwt_payload["id"])
    if err is not None:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message,
        )

    return user


def get_current_active_user(auth_user=Depends(get_current_user)):
    if not auth_user.active:
        raise HTTPException(
            status_code=403,
            detail="user is not active yet",
        )
    return auth_user
