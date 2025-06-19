from fastapi import APIRouter
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