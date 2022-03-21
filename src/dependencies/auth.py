from .db import get_db
from sqlalchemy.orm import Session
from typing import Generator, Optional
from fastapi import Header, HTTPException, Depends
from ..services.auth import RegistrationService, AuthService


def get_registration_service(
    db: Session = Depends(get_db),
) -> Generator[RegistrationService, None, None]:
    try:
        yield RegistrationService(db)
    finally:
        db.close()


def get_auth_service(
    db: Session = Depends(get_db),
) -> Generator[AuthService, None, None]:
    try:
        yield AuthService(db)
    finally:
        db.close()


def validate_jwt(authorization: Optional[str] = Header(None)):
    token = authorization or ""
    if not token.startswith("Bearer "):
        raise HTTPException(
            status_code=400,
            detail="invalid token",
        )

    payload, err = AuthService.verify_jwt(token[7:])
    if err is not None:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message,
        )

    return payload
