from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel
from service.timeset_service import TimestampMixin


class TemplateGroup(SQLModel, TimestampMixin, table=True):
    id: int = Field(default=None, primary_key=True)
    bounding_field: list[dict] = Field(default=None, sa_column=Column(JSON))
    template_group_name: str = Field(nullable=False)
    template_group_threshold:Optional[float]|None = Field(default=None)
    template_container_id: Optional[int]|None = Field(default=None, foreign_key="templatecontainer.id")

