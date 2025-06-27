from typing import Optional
from pydantic import BaseModel

from sqlmodel import SQLModel

class createGroup(BaseModel):
    template_group_name: str
    # template_container_id: int | None = None
    template_group_threshold: float | None = 0.7

class modifyGroup(SQLModel):
    template_group_name: str
    # template_container_id: Optional[int] = None
    template_group_threshold: float | None = 0.7