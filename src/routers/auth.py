from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Response, Cookie, Body
from ..schemas import HTTPError
from ..schemas.user import User
from ..schemas.auth import (
    AuthResponse,
    AuthRequest,
    RefreshRequest,
    RefreshResponse,
    RegisterRequest,
    RecoveryRequest,
)
from ..services.auth import RegistrationService, AuthService
from ..dependencies.auth import get_registration_service, get_auth_service
from ..dependencies.user import get_current_user


router = APIRouter()


@router.post(
    "/register",
    status_code=201,
    responses={500: {"model": HTTPError}},
    tags=["auth"],
)
def register(
    request: RegisterRequest,
    registration_service: RegistrationService = Depends(get_registration_service),
):
    registration_service.register_user(request)
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
def login(
    response: Response,
    auth_request: AuthRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    tokens = auth_service.login(auth_request)

    response.set_cookie(key="refresh_token", value=tokens[1], httponly=True)
    return AuthResponse(jwt_token=tokens[0], refresh_token=tokens[1])


@router.post(
    "/refresh",
    responses={
        200: {"model": RefreshResponse},
        401: {"model": HTTPError},
        500: {"model": HTTPError},
    },
    tags=["auth"],
)
def refresh_authentication(
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

    jwt_token = auth_service.refresh(token)

    return RefreshResponse(jwt_token=jwt_token)


@router.get(
    "/reset",
    responses={
        404: {"model": HTTPError},
        500: {"model": HTTPError},
    },
    tags=["auth"],
)
def get_recovery_phrase(
    user: User = Depends(get_current_user),
    registration_service: RegistrationService = Depends(get_registration_service),
):
    if user.active:
        raise HTTPException(
            status_code=400,
            detail="user already active",
        )

    recovery_phrase = registration_service.generate_recovery_key(user.id)

    return recovery_phrase


@router.post(
    "/activate",
    responses={
        400: {"model": HTTPError},
        404: {"model": HTTPError},
        500: {"model": HTTPError},
    },
    tags=["auth"],
)
def activate_account(
    user: User = Depends(get_current_user),
    registration_service: RegistrationService = Depends(get_registration_service),
    word_list: str = Body(..., embed=True),
):
    if user.active:
        raise HTTPException(
            status_code=400,
            detail="user already active",
        )

    registration_service.activate_user(word_list, user.id)

    return "success"


@router.post(
    "/reset",
    responses={
        400: {"model": HTTPError},
        500: {"model": HTTPError},
    },
    tags=["auth"],
)
def recover_password(
    request: RecoveryRequest,
    registration_service: RegistrationService = Depends(get_registration_service),
):
    registration_service.reset_password(request)

    return "success"
