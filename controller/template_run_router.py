from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
from typing import Optional
import base64


from service import template_run_service

router=APIRouter(prefix="/run",tags=["run_template"])

@router.post("")
async def upload(image: Optional[UploadFile] = File(None)):
    if image is None:
        return Response(content=b"No image uploaded", status_code=400)

    image_data = await template_run_service.uploadImg(image)
    image_data = base64.b64decode(image_data)

    return Response(content=image_data, media_type="image/jpeg")