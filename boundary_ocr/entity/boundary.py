from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field
from typing import Optional, List

class Boundary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    boundary_field: List[int] = Field(sa_column=Column(JSON))
    template_id: Optional[int] = Field(default=None, foreign_key="template.id")