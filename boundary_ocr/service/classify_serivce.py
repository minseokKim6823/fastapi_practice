from typing import Annotated, List
from fastapi import UploadFile,File
from paddleocr import PaddleOCR
import cv2
import numpy as np
import logging

ocr = PaddleOCR(
    lang="korean",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)

async def upload_image_and_classify_by_paddleocr(
    images_list: List[UploadFile],
    boundary_field: List[int]
) -> List[dict]:
    results = []
    x, y, w, h = boundary_field
    for image in images_list:
        image_bytes = await image.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            results.append({"result": None, "error": "이미지를 열 수 없습니다"})
            continue


        cropped_img = img[y:y + h, x:x + w]
        if cropped_img is None or cropped_img.size == 0:
            print("cropped_img 잘못됨", type(cropped_img), cropped_img.shape)
            continue

        ocr_result = ocr.predict(cropped_img)


    return ocr_result[0]["rec_texts"]





