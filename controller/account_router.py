from fastapi import APIRouter

from service import user_service
from model.dto.userDTO import createAccount
from model.dto.userDTO import modifyUserInfo
from model.settings import SessionDep

router = APIRouter()

@router.post("/create_account")
def signUp(user: createAccount , session:SessionDep):
    user_service.createAccount(user,session)
    return "회원가입 완료"

@router.put("/user/{id}")
def updateUserInfo(id: int, updated_data: modifyUserInfo, session: SessionDep):
    user = user_service.modify(id, updated_data, session)
    return user