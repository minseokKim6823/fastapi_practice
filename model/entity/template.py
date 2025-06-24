from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON

class Template(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    template_name: str = Field(default=None, nullable=False)
    image: str = Field(default=None, nullable=False)
    content_type: str = Field(default=None, nullable=False)
    field: list[dict] = Field(sa_column=Column(JSON))
    template_group_id: int = Field(default=0, nullable=True)

