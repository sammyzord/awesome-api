from pydantic import BaseModel, ConstrainedStr, validator


class Username(ConstrainedStr):
    max_length = 25
    min_length = 2


class UserIn(BaseModel):
    username: Username
    password: str
    repeat_password: str

    @validator("repeat_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v


class User(BaseModel):
    id: int
    username: Username
    password: str
    active: bool

    class Config:
        orm_mode = True
