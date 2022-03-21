from sqlalchemy import Column, Integer, String, ForeignKey, event, update
from sqlalchemy.orm import object_session, relationship
from ..database.connection import Base
from ..dependencies.main import get_hashids


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True, index=True, nullable=True)
    title = Column(String(50), nullable=True)
    content = Column(String(1000), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="posts")


@event.listens_for(Post, "after_insert")
def do_stuff(_mapper, _connect, post):
    statement = (
        update(Post)
        .where(Post.id == post.id)
        .values(hash=get_hashids().encode(post.id))
    )

    object_session(post).execute(statement)
