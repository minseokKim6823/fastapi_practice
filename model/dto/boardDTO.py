from sqlmodel import SQLModel

class boardCreate(SQLModel):
    name: str
    image: str
    writer: str

