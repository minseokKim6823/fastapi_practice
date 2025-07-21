from typing import Annotated, List
from fastapi import APIRouter, Depends, UploadFile, File, Form
from boundary_ocr.entity.boundary import Boundary
from boundary_ocr.service.classify_serivce import upload_image_and_classify_by_paddleocr
from model.settings import get_session
router = APIRouter(prefix="/boundary", tags=["boundary"])
result_list =[]
@router.post("/classify/{boundary_id}")
async def classify(
        boundary_id: int,
        images_list: Annotated[List[UploadFile], File(...)],
        session = Depends(get_session),
    ):
    boundary_obj = session.query(Boundary).filter(Boundary.id == boundary_id).first()
    boundary: list[int] = boundary_obj.boundary_field
    results = await upload_image_and_classify_by_paddleocr(images_list,boundary)
    return {"results": results}
