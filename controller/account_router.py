from fastapi import APIRouter, Depends

from service import user_service
from model.dto.userDTO import createAccount
from model.dto.userDTO import modifyUserInfo
from model.settings import SessionDep

router = APIRouter(prefix="/account", tags=["account"])

@router.post("")
def signUp(user: createAccount , session:SessionDep):
    return user_service.createAccount(user,session)


@router.put("/{id}")
def updateUserInfo(id: int, updated_data: modifyUserInfo, session: SessionDep):
    return  user_service.modify(id, updated_data, session)
