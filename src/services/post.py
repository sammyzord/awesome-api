from .main import AppDBService
from ..schemas import DBServiceError
from ..schemas.post import PostIn, PostOut
from ..models.post import Post as PostModel


class PostDBService(AppDBService):
    def create_post(self, post: PostIn):
        try:
            new_post = PostModel(title=post.title, content=post.content)
            self.db.add(new_post)
            self.db.commit()

            self.db.refresh(new_post)

            return PostOut.from_orm(new_post), None

        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))

    def retrieve_post(self, hash: str):
        try:
            post = self.db.query(PostModel).filter(PostModel.hash == hash).first()
            if post is None:
                return None, DBServiceError(status_code=404, message="Post not found")

            return PostOut.from_orm(post), None

        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))
