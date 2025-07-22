import base64
import json
from typing import Optional, List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from model.entity.template import Template
from model.entity.template_group import TemplateGroup
from utils.JSON_converter import convert_list_to_json_dict


async def createTemplate(
        template_name: str,
        image: UploadFile,
        field: str | None,
        template_group_id: int,
        bounding_value: Optional[List[List[str]]],
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

    if bounding_value:
        try:
            bounding_value = convert_list_to_json_dict(bounding_value)
        except json.JSONDecodeError:
            print("JSON 변환 오류 발생")

    template = Template(
        template_group_id=template_group_id,
        template_name=template_name,
        image=encoded,
        content_type=content_type,
        bounding_value=bounding_value,
        field=parsed_field
    )
    session.add(template)
    session.commit()
    return {"id": template.id}


async def updateTemplate(
        id: int,
        template_name: str,
        image: Optional[UploadFile],
        field: str | None,
        template_group_id: int,
        new_template_group_id: int | None,
        bounding_value: Optional[List[List[str]]],
        session: Session
    ):
    template = session.query(Template).filter(
        Template.id == id and
        Template.template_group_id == template_group_id
    ).first()
    if not (template.template_group_id == template_group_id and template.id ==id):
        return "해당 정보에 맞는 템플릿이 없습니다."
    if not field:
        parsed_field = None
    else:
        try:
            parsed_field = json.loads(field)
        except json.JSONDecodeError:
            parsed_field = None

    # 이미지가 실제로 들어왔는지 확인
    if image and image.filename:
        content = await image.read()
        if content:      #사진 없으면 그전 사진
            template.image = base64.b64encode(content).decode()
            template.content_type = image.content_type
    if new_template_group_id:
        template.template_group_id = new_template_group_id

    if bounding_value:
        try:
            bounding_value = convert_list_to_json_dict(bounding_value)
        except json.JSONDecodeError:
            print("JSON 변환 오류 발생")

    template.field =parsed_field
    template.bounding_value = bounding_value
    template.template_name = template_name
    session.commit()
    session.refresh(template)
    return {"id": template.id}

def findImageById(id: int, template_group_id: int, session: Session):
    db_board = session.query(Template).filter(
        Template.id == id and
        Template.template_group_id == template_group_id
        ).first()
    if not (db_board.template_group_id == template_group_id and db_board.id ==id):
        return "해당 정보에 맞는 템플릿이 없습니다."
    return db_board

def findFieldsById(id: int, template_group_id: int, session: Session):
    post = session.query(Template).filter(
        Template.id == id and
        Template.template_group_id == template_group_id
        ).first()
    if not post:
        return None
    if not (post.template_group_id == template_group_id and post.id == id):
        return "해당 정보에 맞는 템플릿이 없습니다."

    template_group = session.query(TemplateGroup).filter(
        TemplateGroup.id == post.template_group_id
    ).first()
    if not (post.template_group_id == template_group_id and post.id == id):
        return "해당 정보에 맞는 템플릿이 없습니다."

    return{
        "id":post.id,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "template_name": post.template_name,
        "field": post.field,
        "template_group_name": template_group.template_group_name if template_group else None,
        "bounding_value": post.bounding_value,
        "template_group_bounding_field": template_group.bounding_field,
        "template_group_id": template_group.id,
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
                "field": post.field,
                "template_group_id": post.template_group_id,
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
            if post.template_group_id == template_group_id:
                template_group = session.query(TemplateGroup).filter(TemplateGroup.id == template_group_id).first()
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
    template = session.query(Template).filter(
        Template.id == id and
        Template.template_group_id == template_group_id
        ).first()
    if not (template.template_group_id == template_group_id and template.id == id):
        return "해당 정보에 맞는 템플릿이 없습니다."
    if template:
        session.delete(template)
        session.commit()
        return {"id": template.id}
    else:
        return "해당 템플릿을 찾을 수 없습니다"


