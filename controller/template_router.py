import base64
import json

from typing import Optional

from fastapi.responses import Response
from model.dto.groupDTO import createGroup, modifyGroup

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from model.entity.template_group import TemplateGroup
from service import template_service, template_group_service
from model.dto.templateDTO import TemplateListResponse
from model.settings import get_session
from utils.JSON_converter import convert_list_to_json_dict
from utils.image_utils import get_image_size_from_uploadfile, normalize_boxes, parse_and_normalize_fields

router = APIRouter(prefix="", tags=["template"])

@router.post("/template")
async def create(
    template_group_name: str,
    bounding_field: Optional[str] = Form(None),
    template_container_id: Optional[int] = None,
    template_group_threshold: Optional[float] = 0.7,
    template_group_id: Optional[int] = Form(None),
    template_name: str = Form(...),
    image: UploadFile = File(...),
    field: Optional[str] = Form(None),
    bounding_value: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    content  = await image.read()
    width, height = get_image_size_from_uploadfile(image)
    encoded_image = base64.b64encode(content).decode()
    content_type = image.content_type
    bf_list  = json.loads(bounding_field) if bounding_field else None
    normalized_bf_boxes = normalize_boxes(bf_list , width, height)
    bv_list = json.loads(bounding_value) if bounding_value else None
    normalized_bv_boxes = convert_list_to_json_dict(bv_list)
    field_json_str = parse_and_normalize_fields(field, width, height)

    templategroup = session.query(TemplateGroup).filter(
        TemplateGroup.id == template_group_id
    ).first()

    if not templategroup:
        group_dto = createGroup(
            template_group_name=template_group_name,
            template_container_id=template_container_id,
            bounding_field=normalized_bf_boxes,
            template_group_threshold=template_group_threshold
        )
        await template_group_service.createTemplateGroup(group_dto, session)
    else:
        group_dto = modifyGroup(
            template_group_name=template_group_name,
            template_container_id=template_container_id,
            bounding_field=normalized_bf_boxes,
            template_group_threshold=template_group_threshold
        )
        await template_group_service.updateTemplateGroup(template_group_id, group_dto, session)

    return await template_service.createTemplate(
        template_name, encoded_image, content_type, field_json_str,
        template_group_id, normalized_bv_boxes, session
    )
@router.put("/{template_group_id}/template/{id}")
async def update(
        id: int,
        template_group_id: int,
        template_group_name: Optional[str] = Form(...),
        bounding_field: Optional[str] = Form(None),
        template_container_id: Optional[int] =Form(None),
        template_group_threshold: Optional[float] = Form(0.7),
        template_name: str = Form(...),
        image: UploadFile = File(...),
        field: Optional[str] = Form(None),
        new_template_group_id: Optional[int] = Form(None),
        bounding_value: Optional[str] = Form(None),
        session: Session = Depends(get_session)
):
    content  = await image.read()
    width, height = get_image_size_from_uploadfile(image)
    encoded_image = base64.b64encode(content).decode()
    content_type = image.content_type

    bf_list = json.loads(bounding_field) if bounding_field else None
    normalized_bf_boxes = normalize_boxes(bf_list, width, height)
    bv_list = json.loads(bounding_value) if bounding_value else None
    normalized_bv_boxes = convert_list_to_json_dict(bv_list)
    field_json_str = parse_and_normalize_fields(field, width, height)

    group_dto = modifyGroup(
        template_group_name=template_group_name,
        template_container_id=template_container_id,
        bounding_field=normalized_bf_boxes,
        template_group_threshold=template_group_threshold
    )
    await template_group_service.updateTemplateGroup(template_group_id, group_dto, session)
    return await template_service.updateTemplate(
        id, template_name, encoded_image, content_type, field_json_str,
        template_group_id, new_template_group_id, normalized_bv_boxes, session
    )
@router.get("/{template_group_id}/image/{id}")
def readImageById(
        id: int,
        template_group_id: int,
        session: Session = Depends(get_session)
    ):
    try:
        post = template_service.findImageById(id, template_group_id, session)
        image_data = base64.b64decode(post.image)
    except Exception:
        return {"error": "템플릿을 찾을 수 없습니다"}


    return Response(content=image_data, media_type=post.content_type)

@router.get("/{template_group_id}/template/{id}")
def readFieldsById(
        id: int,
        template_group_id: int,
        session: Session = Depends(get_session)
    ):
    template = template_service.findFieldsById(id,template_group_id, session)
    if not template:
        return {"error": "게시물을 찾을 수 없습니다"}
    return template


@router.get("/template", response_model=TemplateListResponse)
def readAll(
        session: Session = Depends(get_session),
        offset: int = 1,
        limit: int = 10
    ):
    return template_service.findAll(session, offset, limit)

@router.get("/{template_group_id}/template", response_model=TemplateListResponse)
def readByGroupId(
        template_group_id: int,
        session: Session = Depends(get_session),
        offset: int = 1,
        limit: int = 10
    ):
    return template_service.findByGroupId(template_group_id, session, offset, limit)

@router.delete("/{template_group_id}/template/{id}")
def delete(
        id: int,
        template_group_id: int,
        session: Session = Depends(get_session)
    ):
    return template_service.deleteById(id,template_group_id, session)

