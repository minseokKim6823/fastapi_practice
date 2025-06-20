from sqlmodel import SQLModel

class BoardCreate(SQLModel):
    name: str
    image: str

