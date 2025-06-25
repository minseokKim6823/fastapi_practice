from typing import Optional
from pydantic import BaseModel

from sqlmodel import SQLModel

class createGroup(BaseModel):
    template_group_name: str
    template_container_id: int | None = None

class modifyGroup(SQLModel):
    template_group_name: str
    template_container_id: Optional[int] = None