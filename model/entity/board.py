from sqlmodel import Field, SQLModel

class Board(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None, nullable=False, index=True)
    image: str = Field(default=None, nullable=False)

class BoardCreate(SQLModel):
    name: str
    image: str