from typing import Generator
from .db import get_db
from ..services.post import PostDBService


def get_post_service() -> Generator[PostDBService, None, None]:
    db = get_db()
    try:
        yield PostDBService(db)
    finally:
        db.close()
