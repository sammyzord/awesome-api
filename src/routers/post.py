from fastapi import APIRouter, HTTPException, Depends
from ..schemas import HTTPError
from ..schemas.post import PostIn, PostOut
from ..services.post import PostDBService
from ..dependencies.post import get_post_service


router = APIRouter()


@router.post(
    "",
    status_code=201,
    responses={201: {"model": PostOut}, 500: {"model": HTTPError}},
    tags=["posts"],
)
async def create_post(
    post: PostIn, post_service: PostDBService = Depends(get_post_service)
):

    new_post, err = post_service.create_post(post)
    if err is not None:
        raise HTTPException(
            status_code=500,
            detail=err,
        )

    return new_post
