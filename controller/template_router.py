import base64
from typing import Optional, List

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from service import template_service
from model.dto.templateDTO import TemplatePartialRead, TemplateListResponse
from model.settings import get_session


router = APIRouter(prefix="", tags=["template"])

@router.post("/template")
async def create(
        template_group_id: int,
        template_name: str = Form(...),
        image: UploadFile = File(...),
        field: Optional[str] = Form(None),
        bounding_value = Form(None),
        session: Session = Depends(get_session)
    ):
    return await template_service.createTemplate(template_name, image, field, template_group_id, bounding_value,  session)

@router.put("/{template_group_id}/template/{id}")
async def update(
        id: int,
        template_group_id: int,
        template_name: str = Form(...),
        image: Optional[UploadFile] = File(None),
        field: Optional[str] = Form(None),
        new_template_group_id: Optional[int] = Form(None),
        bounding_value = Form(None),
        session: Session = Depends(get_session)
    ):
    return await template_service.updateTemplate(id, template_name, image, field, template_group_id, new_template_group_id, bounding_value, session)


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

@router.get("/{template_group_id}/template/{id}", response_model=TemplatePartialRead)
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

