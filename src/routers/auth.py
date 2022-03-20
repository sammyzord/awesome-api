from fastapi import APIRouter, HTTPException, Depends, Response
from ..schemas import HTTPError
from ..schemas.user import AuthResponse, AuthUser, UserIn
from ..services.auth import RegistrationService, AuthService
from ..dependencies.auth import get_registration_service, get_auth_service


router = APIRouter()


@router.post(
    "/register",
    status_code=201,
    responses={500: {"model": HTTPError}},
    tags=["auth"],
)
async def register(
    user: UserIn,
    registration_service: RegistrationService = Depends(get_registration_service),
):
    err = registration_service.register_user(user)
    if err is not None:
        raise HTTPException(
            status_code=err[0],
            detail=err[1],
        )
    return "success"


@router.post(
    "/login",
    responses={
        200: {"model": AuthResponse},
        400: {"model": HTTPError},
        500: {"model": HTTPError},
    },
    tags=["auth"],
)
async def login(
    response: Response,
    user: AuthUser,
    auth_service: AuthService = Depends(get_auth_service),
):
    tokens, err = auth_service.login(user)
    if err is not None:
        raise HTTPException(
            status_code=err[0],
            detail=err[1],
        )

    elif tokens is not None:
        return {"jwt_token": tokens[0], "refresh_token": tokens[1]}
