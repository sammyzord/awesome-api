from typing import Optional
from pydantic import BaseModel
from .user import Username


class AuthResponse(BaseModel):
    jwt_token: str
    refresh_token: str


class AuthRequest(BaseModel):
    username: Username
    password: str


class RefreshRequest(BaseModel):
    refresh_token: Optional[str]


class RefreshResponse(BaseModel):
    jwt_token: str
