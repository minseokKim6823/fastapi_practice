from fastapi import APIRouter, UploadFile, File, Depends, Form
from fastapi.responses import Response
from typing import Annotated
from requests import Session

from model.settings import get_session
from service import template_run_service
from service.template_run_service import upload_image_and_classify_from_db

router=APIRouter(prefix="/run",tags=["run_template"])

# @router.post("/upload")
# async def upload(image: Optional[UploadFile] = File(None)):
#     if image is None:
#         return Response(content=b"No image uploaded", status_code=400)
#
#     image_data = await template_run_service.uploadImg(image)
#     image_data = base64.b64decode(image_data)
#
#     return Response(content=image_data, media_type="image/jpeg")


@router.post("/images/match")
async def run_match_images(
        threshold: Annotated[str, Form(...)],
        images_list: Annotated[list[UploadFile], File(...)],
        session: Session = Depends(get_session)
        ):
    result = await upload_image_and_classify_from_db(threshold, images_list, session)
    return result