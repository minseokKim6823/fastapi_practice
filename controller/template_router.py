import json
import base64

from io import BytesIO
from typing import Optional
from PIL import Image

from model.dto.groupDTO import createGroup

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session

from service import template_service, template_group_service
from model.dto.templateDTO import TemplatePartialRead, TemplateListResponse
from model.settings import get_session

router = APIRouter(prefix="", tags=["template"])

def get_image_size_from_uploadfile(upload_file: UploadFile) -> tuple[int, int]:
    contents = upload_file.file.read()
    image = Image.open(BytesIO(contents))
    upload_file.file.seek(0)  # ✅ 읽은 뒤 반드시 되돌려주기
    return image.width, image.height

@router.post("/template")
async def create(
        template_group_name: str,
        bounding_field:Optional[str] = Form(None),
        template_container_id: int | None = None,
        template_group_threshold: float | None = 0.7,
        template_group_id: int| None = Form(None),
        template_name: str = Form(...),
        image: UploadFile = File(...),
        field: Optional[str] = Form(None),
        bounding_value: Optional[str]= Form(None),
        session: Session = Depends(get_session)
    ):
    width, height = get_image_size_from_uploadfile(image)

    bounding_field_list = json.loads(bounding_field) if bounding_field else None
    normalized_boxes = []
    for box in bounding_field_list:
        x, y, w, h = box
        normalized_boxes.append([
            x / width,
            y / height,
            w / width,
            h / height
        ])
    parsed_fields = json.loads(field) if field else []
    for f in parsed_fields:
        if "bbox" in f:
            x, y, w, h = f["bbox"]
            f["bbox"] = [
                x / width,
                y / height,
                w / width,
                h / height
            ]
    field_json_str = json.dumps(parsed_fields, ensure_ascii=False)

    # 3. template_group 생성
    group_dto = createGroup(
        template_group_name=template_group_name,
        template_container_id=template_container_id,
        bounding_field=normalized_boxes,
        template_group_threshold=template_group_threshold
    )
    await template_group_service.createTemplateGroup(group_dto, session)

    # 4. template 생성
    return await template_service.createTemplate(
        template_name, image, field_json_str,
        template_group_id, bounding_value,
        session
    )
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

