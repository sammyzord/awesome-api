from sqlalchemy.orm import Session
from ..database.connection import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    return db
