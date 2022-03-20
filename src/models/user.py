from sqlalchemy import Column, Integer, String, Boolean
from ..database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, index=True)
    active = Column(Boolean, default=False)
    password = Column(String)
    recovery_key = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
