from typing import Annotated, List
from fastapi import APIRouter, Depends, UploadFile, File
from model.entity.template import Template
from boundary_ocr.service.classify_service import upload_image_and_classify_by_paddleocr
from model.entity.template_group import TemplateGroup
from model.settings import get_session
router = APIRouter(prefix="/boundary", tags=["boundary"])
result_list =[]
@router.post("/classify/{template_group_id}")
async def classify(
    template_group_id: int,
    images_list: Annotated[List[UploadFile], File(...)],
    session = Depends(get_session),
):
    group = session.get(TemplateGroup, template_group_id)
    if not group or not group.bounding_field:
        return {"error": "bounding_field가 없습니다."}

    # 연결된 템플릿 조회

    template = session.query(Template).filter(Template.template_group_id == group.id).first()
    if not template or not template.bounding_value:
        return {"error": "연결된 템플릿 또는 bounding_value가 없습니다."}

    matched = await upload_image_and_classify_by_paddleocr(
        images_list,
        group.bounding_field,
        template.bounding_value,
        template.template_name
    )

    return {"matched_template_names": matched}
