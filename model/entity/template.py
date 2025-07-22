from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON
from service.timeset_service import TimestampMixin


class Template(SQLModel, TimestampMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    template_name: str = Field(default=None, nullable=False)
    image: str = Field(default=None, nullable=False)
    content_type: str = Field(default=None, nullable=False)
    field: list[dict] = Field(default=None, sa_column=Column(JSON))
    bounding_value: list[dict] = Field(default=None, sa_column=Column(JSON))
    template_group_id: Optional[int]|None = Field(default=None, foreign_key="templategroup.id")


