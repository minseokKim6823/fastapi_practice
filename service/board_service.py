from sqlalchemy.orm import Session
from model.entity.board import Board,BoardCreate

def createBoard(board: BoardCreate, session:Session):
    db_board = Board(**board.dict())
    session.add(db_board)
    session.commit()
    session.refresh(db_board)
    return "저장 완료"

def findById(id: int, session: Session):
    post = session.query(Board).filter(Board.id == id).first()
    return post

def findAll(session: Session):
    allPosts = session.query(Board).all()
    return allPosts

def deleteById(id: int, session: Session):
    post = session.query(Board).filter(Board.id == id).first()
    if post:
        session.delete(post)
        session.commit()
        return f"{id}번 게시물이 삭제되었습니다"
    else:
        return "글을 찾을 수 없습니다"

def updatePost(id: int, updated_data: BoardCreate, session: Session):
    post = session.query(Board).filter(Board.id == id).first()
    post.name = updated_data.name
    post.image = updated_data.image
    session.commit()
    session.refresh(post)
    return post
