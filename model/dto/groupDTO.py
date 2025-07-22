from typing import Optional, List
from pydantic import BaseModel

from sqlmodel import SQLModel

class createGroup(BaseModel):
    template_group_name: str
    bounding_field: Optional[List[List[int]]]| None = None
    template_container_id: int | None = None
    template_group_threshold: float | None = 0.7

class modifyGroup(SQLModel):
    template_group_name: str
    bounding_field: Optional[List[List[int]]]| None = None
    template_container_id: Optional[int]|None = None
    template_group_threshold: float | None = 0.7