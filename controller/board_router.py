from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from service import board_service
from model.dto.boardDTO import boardCreate
from model.settings import get_session
from service.login_service import get_current_user  # ❗ 인증 함수는 이걸 써야 함

router = APIRouter(prefix="/board", tags=["board"])

@router.post("")
def create(board: boardCreate,  session: Session = Depends(get_session) , current_user: dict = Depends(get_current_user)):
    return board_service.createBoard(board, session)



@router.get("{id}")
def readById(id: int, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)):
    return board_service.findById(id, session)


@router.get("")
def readAll( session: Session = Depends(get_session), offset: int = 0, limit: int = 10, current_user: dict = Depends(get_current_user)):
    return board_service.findAll(session, offset, limit)

@router.delete("{id}")
def delete(id: int,  session: Session = Depends(get_session),  current_user: dict = Depends(get_current_user)):
    return board_service.deleteById(id, session)

@router.put("{id}")
def update(id: int, updated_data: boardCreate,  session: Session = Depends(get_session),  current_user: dict = Depends(get_current_user)):
    return board_service.updatePost(id, updated_data, session)
