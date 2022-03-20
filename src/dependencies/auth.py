import jwt
from .db import get_db
from .main import settings
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
    try:
        token = authorization or ""
        if not token.startswith("Bearer "):
            raise HTTPException(
                status_code=400,
                detail="invalid token",
            )

        jwt.decode(token[7:], settings().secret_key, algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="expired token",
        )
