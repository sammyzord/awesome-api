from sqlalchemy.orm import Session


class DBSessionMixin:
    def __init__(self, db: Session):
        self.db = db


class AppDBService(DBSessionMixin):
    pass
