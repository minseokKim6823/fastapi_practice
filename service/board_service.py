import base64
import json
from fastapi import UploadFile
from fastapi.responses import Response

from sqlalchemy.orm import Session
from model.entity.board import Board
from model.dto.boardDTO import BoardCreate


async def createBoard(
        name: str,
        image: UploadFile,
        field: str,
        session: Session
    ):

    try:
        parsed_field = json.loads(field)
    except json.JSONDecodeError:
        return {"error": "field는 유효한 JSON 문자열이어야 합니다."}

    existing = session.query(Board).filter(Board.name == name).first()
    if existing:
        return {"error": f"이미 존재하는 name입니다: {name}"}

    content = await image.read()
    encoded = base64.b64encode(content).decode()
    content_type = image.content_type

    db_board = Board(
        name=name,
        image=encoded,
        content_type=content_type,
        field=json.dumps(parsed_field),
    )
    session.add(db_board)
    session.commit()
    return "저장완료"

async def updatePost(
        id: int,
        name: str,
        image: UploadFile,
        field: str,
        session: Session
    ):

    try:
        parsed_field = json.loads(field)
    except json.JSONDecodeError:
        return {"error": "field는 유효한 JSON 문자열이어야 합니다."}

    post = session.query(Board).filter(Board.id == id).first()
    if not post:
        return "글을 찾을 수 없습니다"

    existing = session.query(Board).filter(Board.name == name, Board.id != id).first()
    if existing:
        return {"error": f"다른 게시물에서 이미 사용 중인 name입니다: {name}"}


    content = await image.read()
    encoded = base64.b64encode(content).decode()
    content_type = image.content_type

    post.name = name
    post.image = encoded
    post.content_type = content_type
    post.field = json.dumps(parsed_field)

    session.commit()
    session.refresh(post)
    return "수정완료"

def findImageById(id: int, session: Session):
    return session.query(Board).filter(Board.id == id).first()

def findFieldsById(id: int, session: Session):
    return session.query(Board).filter(Board.id == id).first()

def findAll(session: Session, page: int = 1, limit: int = 10):
    if page <= 0:
        return {"error": "페이지는 1부터 시작합니다."}
    else:
        offset = (page - 1) * 10
        total = session.query(Board).count()
        allPosts = session.query(Board).offset(offset).limit(limit).all()
        return {
            "total": total,
            "page": page,
            "posts": [
                {"name": post.name}
                for post in allPosts
            ]
        }

def deleteById(id: int, session: Session):
    post = session.query(Board).filter(Board.id == id).first()
    if post:
        session.delete(post)
        session.commit()
        return f"{id}번 게시물이 삭제되었습니다"
    else:
        return "글을 찾을 수 없습니다"


