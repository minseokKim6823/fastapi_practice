from sqlmodel import SQLModel

class createAccount(SQLModel):
    user_id: str
    password: str

class modifyUserInfo(SQLModel):
    username: str
    image: str