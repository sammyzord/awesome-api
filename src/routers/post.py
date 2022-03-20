from fastapi import APIRouter, HTTPException, Depends
from ..schemas import HTTPError
from ..schemas.post import PostIn, PostOut
from ..services.post import PostDBService
from ..dependencies.auth import validate_jwt
from ..dependencies.post import get_post_service


router = APIRouter()


@router.post(
    "",
    status_code=201,
    responses={201: {"model": PostOut}, 500: {"model": HTTPError}},
    tags=["posts"],
)
async def create_post(
    post: PostIn,
    post_service: PostDBService = Depends(get_post_service),
    user=Depends(validate_jwt),
):

    new_post, err = post_service.create_post(post)
    if err is not None:
        raise HTTPException(
            status_code=err[0],
            detail=err[1],
        )

    return new_post


@router.get(
    "/{hash}",
    status_code=200,
    responses={
        200: {"model": PostOut},
        404: {"model": HTTPError},
        500: {"model": HTTPError},
    },
    tags=["posts"],
)
async def retrieve_post(
    hash: str, post_service: PostDBService = Depends(get_post_service)
):
    post, err = post_service.retrieve_post(hash)
    if err is not None:
        raise HTTPException(
            status_code=err[0],
            detail=err[1],
        )

    return post
