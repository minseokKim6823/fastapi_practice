from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, JSON
from model.entity.template_group import TemplateGroup
from service.timeset_service import TimestampMixin


class Template(SQLModel, TimestampMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    template_name: str = Field(default=None, nullable=False)
    image: str = Field(default=None, nullable=False)
    content_type: str = Field(default=None, nullable=False)
    field: list[dict] = Field(sa_column=Column(JSON)) #리스트 형태로 저장됨
    template_group_id: Optional[int] = Field(default=None, foreign_key="templategroup.id")

    group: Optional[TemplateGroup] = Relationship(back_populates="templates")

