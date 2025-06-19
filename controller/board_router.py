from idlelib.rpc import response_queue

from fastapi import APIRouter
from sqlalchemy.orm import Session

from service import board_service
from model.entity.board import Board, BoardCreate
from model.settings import SessionDep  # ✅ 세션 의존성 import

router  = APIRouter()


@router.post("/board")
def create_board(board: BoardCreate, session: SessionDep):
    db_board = Board(**board.dict())
    session.add(db_board)
    session.commit()
    session.refresh(db_board)
    return db_board

@router.get("/board/{id}")
def findById(id: int, session: SessionDep):
    post = board_service.findById(id, session)
    return post

@router.get("/board")
def findAll(session: SessionDep):
    posts = board_service.findAll(session)
    return posts



