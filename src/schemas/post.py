from typing import Optional
from pydantic import BaseModel


class PostIn(BaseModel):
    title: Optional[str]
    content: str
