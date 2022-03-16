from sqlalchemy import Column, Integer, String, event, update
from sqlalchemy.orm import object_session
from ..database.connection import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True, index=True, nullable=True)
    title = Column(String(50), nullable=True)
    content = Column(String(1000), nullable=False)


@event.listens_for(Post, "after_insert")
def do_stuff(mapper, connect, post):
    # target is an instance of Table

    statement = update(Post).where(Post.id == post.id).values(hash=f"{post.id}blabla")
    object_session(post).execute(statement)
