from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
    active: bool

    class Config:
        orm_mode = True
