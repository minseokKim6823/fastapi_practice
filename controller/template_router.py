import json

from io import BytesIO
from typing import Optional
from PIL import Image

from model.dto.groupDTO import createGroup, modifyGroup

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from service import template_service, template_group_service
from model.dto.templateDTO import TemplatePartialRead, TemplateListResponse
from model.settings import get_session

router = APIRouter(prefix="", tags=["template"])

def get_image_size_from_uploadfile(upload_file: UploadFile) -> tuple[int, int]:
    contents = upload_file.file.read()
    image = Image.open(BytesIO(contents))
    upload_file.file.seek(0)
    return image.width, image.height

def normalize_boxes(boxes, width, height):
    if not boxes:
        return []
    return [
        [x / width, y / height, w / width, h / height]
        for x, y, w, h in boxes
    ]

def parse_and_normalize_fields(field_str, width, height):
    fields = json.loads(field_str) if field_str else []
    if width and height:
        for f in fields:
            if "bbox" in f:
                x, y, w, h = f["bbox"]
                f["bbox"] = [x / width, y / height, w / width, h / height]
    return json.dumps(fields, ensure_ascii=False)

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

    width, height = get_image_size_from_uploadfile(image)
    bounding_field_list = json.loads(bounding_field) if bounding_field else None
    normalized_boxes = normalize_boxes(bounding_field_list, width, height)
    field_json_str = parse_and_normalize_fields(field, width, height)

    group_dto = createGroup(
        template_group_name=template_group_name,
        template_container_id=template_container_id,
        bounding_field=normalized_boxes,
        template_group_threshold=template_group_threshold
    )
    await template_group_service.createTemplateGroup(group_dto, session)

    return await template_service.createTemplate(
        template_name, image, field_json_str,
        template_group_id, bounding_value, session
    )
@router.put("/{template_group_id}/template/{id}")
async def update(
        id: int,
        template_group_id: int,
        template_group_name: str,
        bounding_field: Optional[str] = Form(None),
        template_container_id: Optional[int] = None,
        template_group_threshold: Optional[float] = 0.7,
        template_name: str = Form(...),
        image: Optional[UploadFile] = File(None),
        field: Optional[str] = Form(None),
        new_template_group_id: Optional[int] = Form(None),
        bounding_value: Optional[str] = Form(None),
        session: Session = Depends(get_session)
):
    width, height = get_image_size_from_uploadfile(image) if image else (None, None)
    bounding_field_list = json.loads(bounding_field) if bounding_field else None
    normalized_boxes = normalize_boxes(bounding_field_list, width, height)
    field_json_str = parse_and_normalize_fields(field, width, height)

    group_dto = modifyGroup(
        template_group_name=template_group_name,
        template_container_id=template_container_id,
        bounding_field=normalized_boxes,
        template_group_threshold=template_group_threshold
    )
    await template_group_service.updateTemplateGroup(template_group_id, group_dto, session)

    return await template_service.updateTemplate(
        id, template_name, image,
        field_json_str, template_group_id,
        new_template_group_id, bounding_value, session
    )

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

