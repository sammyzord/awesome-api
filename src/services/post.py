from .main import AppDBService
from ..schemas.post import PostIn, PostOut
from ..models.post import Post


class PostDBService(AppDBService):
    def create_post(self, post: PostIn):
        try:
            new_post = Post(title=post.title, content=post.content)
            self.db.add(new_post)
            self.db.commit()

            self.db.refresh(new_post)

            return PostOut.from_orm(new_post), None

        except Exception as err:
            return None, str(err)
