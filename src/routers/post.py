from fastapi import APIRouter, HTTPException, Depends
from ..schemas import HTTPError
from ..schemas.user import User
from ..schemas.post import PostIn, PostOut
from ..services.post import PostDBService
from ..dependencies.user import get_current_active_user
from ..dependencies.post import get_post_service


router = APIRouter()


@router.post(
    "",
    status_code=201,
    responses={201: {"model": PostOut}, 500: {"model": HTTPError}},
    tags=["posts"],
)
def create_post(
    post: PostIn,
    post_service: PostDBService = Depends(get_post_service),
    user: User = Depends(get_current_active_user),
):

    new_post, err = post_service.create_post(post, user)
    if err is not None:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message,
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
def retrieve_post(hash: str, post_service: PostDBService = Depends(get_post_service)):
    post, err = post_service.retrieve_post(hash)
    if err is not None:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message,
        )

    return post
