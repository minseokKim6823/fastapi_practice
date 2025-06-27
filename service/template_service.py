import base64
import json
from typing import Optional

from fastapi import File, UploadFile
from fastapi.responses import Response

from sqlalchemy.orm import Session
from model.entity.template import Template
# from model.entity.template_container import TemplateContainer
from model.entity.template_group import TemplateGroup


async def createTemplate(
        template_name: str,
        image: UploadFile,
        field: str | None,
        template_group_id: int,
        session: Session
    ):
    if not field:
        parsed_field = None
    else:
        try:
            parsed_field = json.loads(field)
        except json.JSONDecodeError:
            parsed_field = None

    content = await image.read()
    encoded = base64.b64encode(content).decode()
    content_type = image.content_type

    db_board = Template(
        template_name=template_name,
        image=encoded,
        content_type=content_type,
        template_group_id=template_group_id,
        field=parsed_field
    )
    session.add(db_board)
    session.commit()
    return "저장완료"


async def updateTemplate(
        id: int,
        template_name: str,
        image: Optional[UploadFile],
        field: Optional[str],
        template_group_id: int,
        session: Session
    ):
    post = session.query(Template).filter(
        Template.id == id and
        Template.template_group_id == template_group_id
    ).first()
    if not (post.template_group_id == template_group_id and post.id ==id):
        return "해당 정보에 맞는 템플릿이 없습니다."
    else:
        try:
            parsed_field = json.loads(field)
        except json.JSONDecodeError:
            parsed_field = None

    # 이미지가 실제로 들어왔는지 확인
    if image and image.filename:
        content = await image.read()
        if content:      #사진 없으면 그전 사진
            post.image = base64.b64encode(content).decode()
            post.content_type = image.content_type

    post.field =parsed_field
    post.template_name = template_name
    session.commit()
    session.refresh(post)
    return "수정완료"

def findImageById(id: int, template_group_id: int, session: Session):
    return session.query(Template).filter(
        Template.id == id and
        Template.template_group_id == template_group_id
        ).first()

def findFieldsById(id: int, template_group_id: int, session: Session):
    post = session.query(Template).filter(
        Template.id == id and
        Template.template_group_id == template_group_id
        ).first()
    if not post:
        return None

    template_group = session.query(TemplateGroup).filter(
        TemplateGroup.id == post.template_group_id
    ).first()

    # if template_group:
    #     template_container = session.query(TemplateContainer).filter(
    #         TemplateContainer.id == template_group.template_container_id
    #     ).first()
    # else:
    #     template_container = None

    return{
        "id": post.id,
        "template_name": post.template_name,
        "field": post.field if post.field is not None else [],
        "template_group_id": post.template_group_id if template_group else None,
        "template_group_name": template_group.template_group_name if template_group else None,
        # "template_container_name": template_container.template_container_name if template_container else None,
        # "template_container_id": template_container.id if template_container else None
    }



def findAll(session: Session, page: int = 1, limit: int = 10):
    if page <= 0:
        return {"error": "페이지는 1부터 시작합니다."}
    else:
        offset = (page - 1) * limit
        total = session.query(Template).count()
        allPosts = session.query(Template).offset(offset).limit(limit).all()
        result = []
        for post in allPosts:
            template_group = session.query(TemplateGroup).filter(TemplateGroup.id == post.template_group_id).first()
            result.append({
                "id":post.id,
                "created_at": post.created_at,
                "updated_at": post.updated_at,
                "template_name": post.template_name,
                "template_group_id": post.template_group_id,
                "field":post.field,
                "template_group_name": template_group.template_group_name if template_group else None
            })
        return {
            "total": total,
            "page": page,
            "posts": result
        }

def findByGroupId(template_group_id: int, session: Session, page: int = 1, limit: int = 10):
    if page <= 0:
        return {"error": "페이지는 1부터 시작합니다."}
    else:
        offset = (page - 1) * limit
        total = session.query(Template).count()
        allPosts = session.query(Template).offset(offset).limit(limit).all()

        result = []
        for post in allPosts:
            print(post.template_group_id)
            print(TemplateGroup.id)
            template_group = session.query(TemplateGroup).filter(
                post.template_group_id == TemplateGroup.id
            ).first()
            print(template_group)
            result.append({
                "id": post.id,
                "created_at": post.created_at,
                "updated_at": post.updated_at,
                "field": post.field,
                "template_name": post.template_name,
                "template_group_id": post.template_group_id,
                "template_group_name": template_group.template_group_name if template_group else None
            })
        return {
            "total": total,
            "page": page,
            "posts": result
        }

def deleteById(id: int, template_group_id: int, session: Session):
    post = session.query(Template).filter(
        Template.id == id and
        Template.template_group_id == template_group_id
        ).first()
    if post:
        session.delete(post)
        session.commit()
        return f"{id}번 게시물이 삭제되었습니다"
    else:
        return "해당 템플릿을 찾을 수 없습니다"


