from sqlmodel import SQLModel

class createContainer(SQLModel):
    container_name: str

class modifyContainer(SQLModel):
    container_name: str