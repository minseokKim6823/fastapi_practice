import base64
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from service import template_service
from model.dto.templateDTO import TemplatePartialRead, TemplateListResponse
from model.settings import get_session

# from fastapi.security import OAuth2PasswordBearer
# from service.login_service import get_current_user

router = APIRouter(prefix="/template", tags=["template"])

@router.post("/{template_group_id}")
async def create(
        template_group_id: int,
        template_name: str = Form(...),
        image: UploadFile = File(...),
        field: Optional[str] = Form(None),
        session: Session = Depends(get_session)
    ):
    return await template_service.createTemplate(template_name, image, field, template_group_id, session)

@router.put("/{template_group_id}/{id}")
async def update(
        id: int,
        template_group_id: int,
        template_name: str = Form(...),
        image: Optional[UploadFile] = File(None),
        field: Optional[str] = Form(None),
        session: Session = Depends(get_session)
    ):
    return await template_service.updateTemplate(id, template_name, image, field, template_group_id, session)


@router.get("/image/{template_group_id}/{id}")
def readImageById(
        id: int,
        template_group_id: int,
        session: Session = Depends(get_session)
    ):
    post = template_service.findImageById(id, template_group_id, session)
    try:
        image_data = base64.b64decode(post.image)
    except Exception:
        return {"error": "이미지 디코딩 실패"}

    return Response(content=image_data, media_type=post.content_type)

@router.get("/{template_group_id}/{id}", response_model=TemplatePartialRead)
def readFieldsById(
        id: int,
        template_group_id: int,
        session: Session = Depends(get_session)
    ):
    template = template_service.findFieldsById(id,template_group_id, session)
    if not template:
        return {"error": "게시물을 찾을 수 없습니다"}
    return template


@router.get("", response_model=TemplateListResponse)
def readAll(
        session: Session = Depends(get_session),
        offset: int = 1,
        limit: int = 10
    ):
    return template_service.findAll(session, offset, limit)

@router.get("/{template_group_id}", response_model=TemplateListResponse)
def readByGroupId(
        template_group_id: int,
        session: Session = Depends(get_session),
        offset: int = 1,
        limit: int = 10
    ):
    return template_service.findByGroupId(template_group_id, session, offset, limit)

@router.delete("/{template_group_id}/{id}")
def delete(
        id: int,
        template_group_id: int,
        session: Session = Depends(get_session)
    ):
    return template_service.deleteById(id,template_group_id, session)

