from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
# from model.entity.template_container import TemplateContainer
from service.timeset_service import TimestampMixin


class TemplateGroup(SQLModel, TimestampMixin, table=True):
    id: int = Field(default=None, primary_key=True)
    template_group_name: str = Field(nullable=False)
    template_group_threshold:Optional[float]|None = Field(default=None)
    # template_container_id: Optional[int]|None = Field(default=None, foreign_key="templatecontainer.id")

    # container: Optional[TemplateContainer] = Relationship(back_populates="groups")
    templates: List["Template"] = Relationship(back_populates="group")
