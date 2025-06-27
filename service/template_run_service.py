import base64
from io import BytesIO
from PIL import Image

from fastapi import UploadFile
from sqlalchemy.orm import Session

import imagehash

from model.entity.template import Template
# from model.entity.template_container import TemplateContainer
from model.entity.template_group import TemplateGroup


# async def uploadImg(image: UploadFile):
#     img = await image.read()
#     return base64.b64encode(img).decode()

async def upload_image_and_classify_from_db(
        # template_container_id: int | None,
        template_group_id: str | None,
        threshold: float | None,
        images_list: list[UploadFile],
        session: Session,
) -> list[dict]:
    results = []

    if template_group_id is None:
        templates = session.query(Template).all()
    else:
        templates = session.query(Template).filter(
            TemplateGroup.id ==template_group_id
        ).all()

    for image in images_list:
        uploaded_bytes = await image.read()
        try:
            uploaded_image = Image.open(BytesIO(uploaded_bytes))
            uploaded_hash = imagehash.average_hash(uploaded_image, hash_size=128)
        except Exception as e:
            results.append({
                "filename": image.filename,
                "error": f"이미지를 열 수 없습니다: {e}"
            })
            continue

        best_match = None
        best_score = -1.0
        best_group = None
        best_threshold = 0.7

        for template in templates:
            try:
                decoded = base64.b64decode(template.image)
                template_image = Image.open(BytesIO(decoded))
                template_hash = imagehash.average_hash(template_image, hash_size=128)
                diff = uploaded_hash - template_hash
                similarity = 1 - (diff / (128**2))

                group = session.query(TemplateGroup).filter(
                    TemplateGroup.id == template.template_group_id
                ).first()

                template_threshold = (
                    threshold
                    if threshold is not None
                    else group.template_group_threshold if group and group.template_group_threshold is not None
                    else 0.7
                )

                print(f"[→] Template ID {template.id} 유사도: {similarity:.4f}, 기준: {template_threshold:.2f}")

                if similarity >= template_threshold and similarity > best_score:
                    best_score = similarity
                    best_match = template
                    best_group = group
                    best_threshold = template_threshold

            except Exception as e:
                print(f"[!] 이미지 비교 실패 - Template ID {template.id}: {e}")

            results.append({
                "filename": image.filename,
                "matched": True,
                "template_id": best_match.id,
                "template_name": best_match.template_name,
                "similarity": round(best_score, 4),
                "template_group_name": best_group.template_group_name if best_group else None,
                "template_group_id": best_group.id if best_group else None,
                "threshold": round(best_threshold, 2)
            })
        else:
            results.append({
                "result": "이미지가 없습니다."
            })

    return results
