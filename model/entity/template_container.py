from typing import List
from sqlmodel import Field, SQLModel, Relationship
from service.timeset_service import TimestampMixin

class TemplateContainer(SQLModel, TimestampMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    template_container_name: str = Field(default=None, nullable=False)

    groups: List["TemplateGroup"] = Relationship(back_populates="container")