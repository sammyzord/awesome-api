from fastapi import APIRouter
from ..schemas.post import PostIn

router = APIRouter()


@router.post("/", tags=["posts"])
async def create_post(post: PostIn):
    return post
