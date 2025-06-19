from sqlalchemy.orm import Session
from model.entity.board import Board


def findById(id: int, session: Session):
    post = session.query(Board).filter(Board.id == id).first();
    return post

def findAll(session: Session):
    allPosts = session.query(Board).all()
    return allPosts



