from .main import AppDBService
from ..schemas.post import PostIn
from ..models.post import Post


class PostDBService(AppDBService):
    def create_post(self, post: PostIn):
        new_post = Post(title=post.title, content=post.content)
        self.db.add(new_post)
        self.db.commit()
