from datetime import datetime
from typing import List, Dict, Optional

from pydantic import BaseModel

class TemplateCreate(BaseModel):
    template_name: str

class TemplatePartialRead(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    field: Optional[list] = None
    template_name: str
    template_group_id: Optional[int] = None
    template_group_name: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S") if v else None
        }


class TemplateListResponse(BaseModel):
    total: int
    page: int
    posts: List[TemplatePartialRead]