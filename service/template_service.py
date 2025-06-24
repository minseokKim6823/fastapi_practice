import base64
import json
from typing import Optional

from fastapi import File, UploadFile
from fastapi.responses import Response

from sqlalchemy.orm import Session
from model.entity.template import Template
from model.dto.templateDTO import TemplateCreate


async def createTemplate(
        name: str,
        image: UploadFile,
        field: str,
        group_id: int,
        session: Session
    ):

    try:
        parsed_field = json.loads(field)
    except json.JSONDecodeError:
        return {"error": "field는 유효한 JSON 문자열이어야 합니다."}

    existing = session.query(Template).filter(Template.name == name).first()
    if existing:
        return {"error": f"이미 존재하는 name입니다: {name}"}

    content = await image.read()
    encoded = base64.b64encode(content).decode()
    content_type = image.content_type

    db_board = Template(
        name=name,
        image=encoded,
        content_type=content_type,
        group_id=group_id,
        field=json.dumps(parsed_field),
    )
    session.add(db_board)
    session.commit()
    return "저장완료"

async def updatePost(
        id: int,
        name: str,
        image: Optional[UploadFile],
        field: str,
        group_id: int,
        session: Session
    ):
    post = session.query(Template).filter(Template.id == id).first()
    # 있는지
    if not post:
        return "글을 찾을 수 없습니다."

    # 중복방지
    existing = session.query(Template).filter(Template.name == name, Template.id != id).first()
    if existing:
        return {"error": f"다른 게시물에서 이미 사용 중인 name입니다: {name}"}

    # JSON 형태
    try:
        parsed_field = json.loads(field)
    except json.JSONDecodeError:
        return {"error": "field는 유효한 JSON 문자열이어야 합니다."}

    # 이미지가 실제로 들어왔는지 확인
    if image and image.filename:
        content = await image.read()
        if content:      #사진 없으면 그전 사진
            post.image = base64.b64encode(content).decode()
            post.content_type = image.content_type

    post.name = name
    post.group_id = group_id
    post.field = parsed_field

    session.commit()
    session.refresh(post)
    return "수정완료"

def findImageById(id: int, session: Session):
    return session.query(Template).filter(Template.id == id).first()

def findFieldsById(id: int, session: Session):
    return session.query(Template).filter(Template.id == id).first()

def findAll(session: Session, page: int = 1, limit: int = 10):
    if page <= 0:
        return {"error": "페이지는 1부터 시작합니다."}
    else:
        offset = (page - 1) * 10
        total = session.query(Template).count()
        allPosts = session.query(Template).offset(offset).limit(limit).all()
        return {
            "total": total,
            "page": page,
            "posts": [
                {"name": post.name}
                for post in allPosts
            ]
        }

def deleteById(id: int, session: Session):
    post = session.query(Template).filter(Template.id == id).first()
    if post:
        session.delete(post)
        session.commit()
        return f"{id}번 게시물이 삭제되었습니다"
    else:
        return "글을 찾을 수 없습니다"


