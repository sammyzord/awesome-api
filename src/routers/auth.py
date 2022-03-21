from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Response, Cookie
from ..schemas import HTTPError
from ..schemas.user import UserIn
from ..schemas.auth import AuthResponse, AuthRequest, RefreshRequest, RefreshResponse
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
    auth_request: AuthRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    tokens, err = auth_service.login(auth_request)
    if err is not None:
        raise HTTPException(
            status_code=err[0],
            detail=err[1],
        )

    elif tokens is not None:
        response.set_cookie(key="refresh_token", value=tokens[1], httponly=True)
        return AuthResponse(jwt_token=tokens[0], refresh_token=tokens[1])


@router.post(
    "/{user_id}/refresh",
    responses={
        200: {"model": RefreshResponse},
        401: {"model": HTTPError},
        500: {"model": HTTPError},
    },
    tags=["auth"],
)
async def refresh_authentication(
    user_id: int,
    refresh_request: RefreshRequest,
    refresh_token: Optional[str] = Cookie(None),
    auth_service: AuthService = Depends(get_auth_service),
):
    token = refresh_request.refresh_token or refresh_token
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="no token provided",
        )

    jwt_token, err = auth_service.refresh(user_id, token)
    if err is not None:
        raise HTTPException(
            status_code=err[0],
            detail=err[1],
        )

    elif jwt_token is not None:
        return RefreshResponse(jwt_token=jwt_token)
