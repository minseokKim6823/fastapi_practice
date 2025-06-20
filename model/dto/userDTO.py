from sqlmodel import SQLModel

class login(SQLModel):
    user_id: str
    password: str

class createAccount(SQLModel):
    user_id: str
    password: str

class modifyUserInfo(SQLModel):
    name: str
    image: str