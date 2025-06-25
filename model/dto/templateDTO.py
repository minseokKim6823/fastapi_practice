from typing import List,Dict

from pydantic import BaseModel

class TemplateCreate(BaseModel):
    template_name: str

class TemplateCreate(BaseModel):
    template_name: str

class TemplateListResponse(BaseModel):
    total: int
    page: int
    posts: List[TemplateCreate]


class TemplatePartialRead(BaseModel):
    template_name: str
    field: List[Dict]
