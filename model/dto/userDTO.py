from sqlmodel import SQLModel

class createAccount(SQLModel):
    user_id: str
    password: str

class modifyUserInfo(SQLModel):
    name: str
    image: str