import base64

from fastapi import File, UploadFile
from fastapi.responses import Response

from sqlalchemy.orm import Session

async def uploadImg(
        image: UploadFile,
):
    img = await image.read()
    encoded_img=base64.b64encode(img).decode()
    return encoded_img