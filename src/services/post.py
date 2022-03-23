from .main import AppDBService
from ..schemas import DBServiceError
from ..schemas.post import PostIn, PostOut
from ..models.post import Post as PostModel
from sqlalchemy.orm import load_only


class PostDBService(AppDBService):
    def create_post(self, post: PostIn, user_id: int):
        try:
            new_post = PostModel(
                title=post.title, content=post.content, user_id=user_id
            )
            self.db.add(new_post)
            self.db.commit()

            self.db.refresh(new_post)

            return PostOut.from_orm(new_post), None

        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))

    def retrieve_post(self, hash: str):
        try:
            post = self.db.query(PostModel).filter(PostModel.hash == hash).one_or_none()
            if post is None:
                return None, DBServiceError(status_code=404, message="Post not found")

            return PostOut.from_orm(post), None

        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))

    def comment_post(self, post: PostIn, parent_hash: str, user_id: int):
        try:
            query = (
                self.db.query(PostModel)
                .filter(PostModel.hash == parent_hash)
                .options(load_only("id"))
                .one_or_none()
            )
            if query is None:
                return None, DBServiceError(status_code=404, message="Post not found")

            new_post = PostModel(
                title=post.title,
                content=post.content,
                user_id=user_id,
                parent_id=query.id,
            )

            self.db.add(new_post)
            self.db.commit()

            self.db.refresh(new_post)

            return PostOut.from_orm(new_post), None

        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))
