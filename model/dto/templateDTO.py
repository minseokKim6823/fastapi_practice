from typing import List, Dict, Optional

from pydantic import BaseModel

class TemplateCreate(BaseModel):
    template_name: str

class TemplateCreate(BaseModel):
    template_name: str


class TemplatePartialRead(BaseModel):
    template_name: str
    template_group_id: int
    template_group_name: Optional[str] = None
    template_container_name: Optional[str] = None
    template_container_id: Optional[int] = None

class TemplateListResponse(BaseModel):
    total: int
    page: int
    posts: List[TemplatePartialRead]