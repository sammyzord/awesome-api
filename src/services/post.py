from .main import AppDBService
from ..schemas.post import PostIn, PostOut
from ..models.post import Post as PostModel
from sqlalchemy.orm import load_only
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException


class PostDBService(AppDBService):
    def create_post(self, post: PostIn, user_id: int):
        try:
            new_post = PostModel(
                title=post.title, content=post.content, user_id=user_id
            )
            self.db.add(new_post)
            self.db.commit()

            self.db.refresh(new_post)

            return PostOut.from_orm(new_post)

        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    def retrieve_post(self, hash: str):
        try:
            post = self.db.query(PostModel).filter(PostModel.hash == hash).one()
            return PostOut.from_orm(post)

        except NoResultFound:
            raise HTTPException(status_code=404, detail="Post not found")
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    def comment_post(self, post: PostIn, parent_hash: str, user_id: int):
        try:
            query = (
                self.db.query(PostModel)
                .filter(PostModel.hash == parent_hash)
                .options(load_only("id"))
                .one()
            )

            new_post = PostModel(
                title=post.title,
                content=post.content,
                user_id=user_id,
                parent_id=query.id,
            )

            self.db.add(new_post)
            self.db.commit()

            self.db.refresh(new_post)

            return PostOut.from_orm(new_post)

        except NoResultFound:
            raise HTTPException(status_code=404, detail="Post not found")
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
