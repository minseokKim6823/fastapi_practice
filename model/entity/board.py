from sqlmodel import Field, SQLModel

class Board(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None, nullable=False)
    image: str = Field(default=None, nullable=False)
    content_type: str = Field(default=None, nullable=False)
    field: str = Field(default=None, nullable=True)

