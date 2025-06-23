import base64
from fastapi import UploadFile
from fastapi.responses import Response

from sqlalchemy.orm import Session
from model.entity.board import Board
from model.dto.boardDTO import boardCreate


async def createBoard(name: str, writer: str, image: UploadFile, session: Session):
    content = await image.read()
    encoded = base64.b64encode(content).decode()
    content_type = image.content_type

    db_board = Board(
        name=name,
        writer=writer,
        image=encoded,
        content_type=content_type,
    )
    session.add(db_board)
    session.commit()
    session.refresh(db_board)
    return db_board

def findById(id: int, session: Session):
    return session.query(Board).filter(Board.id == id).first()

def findAll(board: boardCreate, session: Session, page: int = 1, limit: int = 10):
    if page <= 0:
        return {"error": "페이지는 1부터 시작합니다."}
    else:
        offset = (page - 1) * 10
        total = session.query(board).count()
        allPosts = session.query(board).offset(offset).limit(limit).all()
        return {
            "total": total,
            "page": page,
            "posts": allPosts
        }

def deleteById(id: int, session: Session):
    post = session.query(Board).filter(Board.id == id).first()
    if post:
        session.delete(post)
        session.commit()
        return f"{id}번 게시물이 삭제되었습니다"
    else:
        return "글을 찾을 수 없습니다"

def updatePost(id: int, updated_data: boardCreate, session: Session):
    post = session.query(Board).filter(Board.id == id).first()
    if not post:
        return "글을 찾을 수 없습니다"
    post.name = updated_data.name
    post.image = updated_data.image
    session.commit()
    session.refresh(post)
    return post
