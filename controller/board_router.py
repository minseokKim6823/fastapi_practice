from fastapi import APIRouter

from service import board_service
from model.dto.boardDTO import boardCreate
from model.settings import SessionDep  # ✅ 세션 의존성 import

router  = APIRouter()


@router.post("/board")
def create(board: boardCreate, session: SessionDep):
    board_service.createBoard(board,session)
    return "저장이 완료되었습니다."

@router.get("/board/{id}")
def readById(id: int, session: SessionDep):
    post = board_service.findById(id, session)
    return post

@router.get("/board")
def readAll(session: SessionDep, offset: int = 0, limit: int = 10):
    posts = board_service.findAll(session, offset, limit)
    return posts

@router.delete("/board/{id}")
def delete(id: int, session: SessionDep):
    response = board_service.deleteById(id, session)
    return response

@router.put("/board/{id}")
def update(id: int, updated_data: boardCreate, session: SessionDep):
    post = board_service.updatePost(id, updated_data, session)
    return post
