from .db import get_db
from ..services.post import PostDBService


def get_post_service() -> PostDBService:
    db_gen = get_db()
    db = next(db_gen)
    return PostDBService(db)
