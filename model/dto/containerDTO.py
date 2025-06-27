from sqlmodel import SQLModel

class createContainer(SQLModel):
    template_container_name: str

class modifyContainer(SQLModel):
    template_container_name: str