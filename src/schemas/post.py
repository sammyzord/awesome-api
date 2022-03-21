from typing import Optional
from .user import UserOut
from pydantic import BaseModel, ConstrainedStr


class Title(ConstrainedStr):
    max_length = 50


class Content(ConstrainedStr):
    max_length = 1000
    min_length = 5


class PostIn(BaseModel):
    title: Optional[Title]
    content: Content


class PostOut(PostIn):
    hash: str
    user: Optional[UserOut]

    class Config:
        orm_mode = True
