from typing import Generator
from .db import get_db
from ..services.auth import RegistrationService, AuthService


def get_registration_service() -> Generator[RegistrationService, None, None]:
    db = get_db()
    try:
        yield RegistrationService(db)
    finally:
        db.close()


def get_auth_service() -> Generator[AuthService, None, None]:
    db = get_db()
    try:
        yield AuthService(db)
    finally:
        db.close()
