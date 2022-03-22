from typing import Optional
from pydantic import BaseModel, ConstrainedStr, validator


class Username(ConstrainedStr):
    max_length = 25
    min_length = 2


class ConfirmPassword(BaseModel):
    password: str
    repeat_password: str

    @validator("repeat_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v


class RegisterRequest(ConfirmPassword):
    username: Username


class RecoveryRequest(RegisterRequest):
    recovery_key: str


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
