from typing import List, Dict
from fastapi import UploadFile
from paddleocr import PaddleOCR
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

ocr = PaddleOCR(
    lang="korean",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)

async def upload_image_and_classify_by_paddleocr(
    images_list: List[UploadFile],
    bounding_dict: Dict[str, List[float]],
    bounding_value: Dict[str, List[str]],
    template_name: str,
) -> List[str]:
    matched_templates: List[str] = []

    for upload in images_list:
        image_bytes = await upload.read()
        if not image_bytes:
            continue

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        pil_img = Image.open(BytesIO(image_bytes))
        img_width, img_height = pil_img.size

        ocr_result_by_key: Dict[str, List[str]] = {}

        for key, rel_box in bounding_dict.items():
            x_rel, y_rel, w_rel, h_rel = rel_box
            x = int(x_rel * img_width)
            y = int(y_rel * img_height)
            w = int(w_rel * img_width)
            h = int(h_rel * img_height)

            cropped = img[y:y+h, x:x+w]
            if cropped is None or cropped.size == 0:
                continue

            # 디버깅용 저장
            filename = f"cropped_{key}_{x}_{y}_{w}_{h}.jpg"
            cv2.imwrite(filename, cropped)
            print(f"[DEBUG] Saved: {filename}")

            ocr_result = ocr.predict(cropped)
            ocr_texts: List[str] = []
            for block in ocr_result:
                ocr_texts.extend(block["rec_texts"])
            ocr_result_by_key[key] = ocr_texts

        # OCR 결과가 모든 bounding_value와 일치하면 템플릿 이름 저장
        is_match = True
        for key, target_values in bounding_value.items():
            ocr_texts = ocr_result_by_key.get(key, [])
            if not any(ocr_text.strip() in target_values for ocr_text in ocr_texts):
                is_match = False
                break

        if is_match:
            matched_templates.append(template_name)

    return matched_templates
