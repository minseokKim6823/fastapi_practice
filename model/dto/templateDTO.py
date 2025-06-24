from typing import List,Dict

from pydantic import BaseModel

class TemplateCreate(BaseModel):
    name: str

class TemplateListResponse(BaseModel):
    total: int
    page: int
    posts: List[TemplateCreate]


class TemplatePartialRead(BaseModel):
    name: str
    field: List[Dict]
