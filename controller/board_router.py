from fastapi import APIRouter

from service import board_service
from model.entity.board import Board, BoardCreate
from model.settings import SessionDep  # ✅ 세션 의존성 import

router  = APIRouter()


@router.post("/board")
def create_board(board: BoardCreate, session: SessionDep):
    board_service.createBoard(board,session)
    return "저장이 완료되었습니다."

@router.get("/board/{id}")
def findById(id: int, session: SessionDep):
    post = board_service.findById(id, session)
    return post

@router.get("/board")
def findAll(session: SessionDep):
    posts = board_service.findAll(session)
    return posts

@router.delete("/board/{id}")
def deleteById(id: int, session: SessionDep):
    response = board_service.deleteById(id, session)
    return response

@router.put("/board/{id}")
def updateById(id: int, updated_data: BoardCreate, session: SessionDep):
    post = board_service.updatePost(id, updated_data, session)
    return post
