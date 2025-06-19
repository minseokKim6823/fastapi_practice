from sqlalchemy.orm import Session
from model.entity.board import Board


def findById(id: int, session: Session):
    post = session.query(Board).filter(Board.id == id).first();
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


