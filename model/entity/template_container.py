from sqlmodel import Field, SQLModel
from service.timeset_service import TimestampMixin

class TemplateContainer(SQLModel, TimestampMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    template_container_name: str = Field(default=None, nullable=False)

