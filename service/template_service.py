import base64
import json
from typing import Optional, List

from sqlalchemy.orm import Session

from model.entity.template import Template
from model.entity.template_group import TemplateGroup
from utils.image_utils import get_image_size_from_uploadfile, re_normalize_boxes, re_parse_and_normalize_fields


async def createTemplate(
        template_name: str,
        image: str,
        content_type: Optional[str],
        field: str | None,
        template_group_id: int,
        bounding_value: Optional[List[List[str]]],
        session: Session
    ):
    if field:
        try:
            parsed_field = json.loads(field)
        except json.JSONDecodeError:
            parsed_field = None
    else:
        parsed_field = None

    template = Template(
        template_group_id=template_group_id,
        template_name=template_name,
        image=image,
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
    image: str,
    content_type: Optional[str],
    field: str | None,
    template_group_id: int,
    new_template_group_id: int| None,
    bounding_value: Optional[List[List[str]]],
    session: Session
):
    template = session.query(Template).filter_by(
        id=id, template_group_id=template_group_id
    ).first()
    if not template:
        return "해당 템플릿을 찾을 수 없습니다."

    if field:
        try:
            parsed_field = json.loads(field)
        except json.JSONDecodeError:
            parsed_field = None
    else:
        parsed_field = None

    template.template_group_id=new_template_group_id
    template.template_name=template_name
    template.image=image
    template.content_type=content_type
    template.bounding_value=bounding_value
    template.field=parsed_field

    session.commit()
    return {"message": "업데이트 완료"}

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
        TemplateGroup.id == template_group_id
    ).first()
    if not (post.template_group_id == template_group_id and post.id == id):
        return "해당 정보에 맞는 템플릿이 없습니다."
    image = post.image
    image = base64.b64decode(image) if image else None
    width, height = get_image_size_from_uploadfile(image) if image else (None, None)
    bounding_field_list = template_group.bounding_field if template_group.bounding_field else None
    field_list = re_normalize_boxes(bounding_field_list, width, height)
    post.field = re_parse_and_normalize_fields(post.field, width, height)
    post.field = json.loads(post.field)
    return{
        "id":post.id,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "template_name": post.template_name,
        "field": post.field,
        "template_group_name": template_group.template_group_name if template_group.template_group_name else None,
        "bounding_value": post.bounding_value,
        "template_group_bounding_field": field_list,
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


