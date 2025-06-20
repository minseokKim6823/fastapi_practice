from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str | None = Field(default=None)
    username: str = Field(default=None, nullable=True)
    image: str = Field(default=None, nullable=True)
    password: str = Field(default=None, nullable=False)

