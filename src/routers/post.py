from fastapi import APIRouter, Depends
from ..schemas.post import PostIn
from ..dependencies.post import get_post_service
from ..services.post import PostDBService

router = APIRouter()


@router.post("", tags=["posts"])
async def create_post(
    post: PostIn, post_service: PostDBService = Depends(get_post_service)
):
    post_service.create_post(post)
    return "sucesso"
