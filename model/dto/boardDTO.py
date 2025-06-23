from typing import List

from sqlmodel import SQLModel
from pydantic import BaseModel

class BoardCreate(BaseModel):
    name: str

class BoardListResponse(BaseModel):
    total: int
    page: int
    posts: List[BoardCreate]


class BoardPartialRead(BaseModel):
    name: str
    field: str
