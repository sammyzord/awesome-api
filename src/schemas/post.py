from typing import List, Optional
from .user import UserOut
from pydantic import BaseModel, ConstrainedStr


class Title(ConstrainedStr):
    max_length = 50


class Content(ConstrainedStr):
    max_length = 1000
    min_length = 5


class PostBase(BaseModel):
    title: Optional[Title]
    content: Content


class PostIn(PostBase):
    pass


class ParentPost(PostBase):
    hash: str
    user: Optional[UserOut]

    class Config:
        orm_mode = True


class ChildPost(ParentPost):
    pass

    class Config:
        orm_mode = True


class PostOut(PostIn):
    hash: str
    user: Optional[UserOut]
    parent: Optional[ParentPost]
    children: List[ChildPost]

    class Config:
        orm_mode = True
