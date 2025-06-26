import base64
from io import BytesIO
from PIL import Image

from fastapi import UploadFile
from sqlalchemy.orm import Session

import imagehash

from model.entity.template import Template
from model.entity.template_container import TemplateContainer
from model.entity.template_group import TemplateGroup


async def uploadImg(image: UploadFile):
    img = await image.read()
    return base64.b64encode(img).decode()

async def upload_image_and_classify_from_db(
        images_list: list[UploadFile],
        session: Session,
        threshold: float = 0.5
) -> list[dict]:

    results = []

    templates = session.query(Template).all()

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

        for template in templates:
            try:
                decoded =base64.b64decode(template.image)
                template_image = Image.open(BytesIO(decoded))
                template_hash = imagehash.average_hash(template_image, hash_size=128)
                diff = uploaded_hash -template_hash
                similarity = 1 - (diff/(128**2))

                print(f"[→] Template ID {template.id} 유사도: {similarity:.4f}")

                if similarity > best_score:
                    best_score = similarity
                    best_match = template

            except Exception as e:
                print(f"[!] 이미지 비교 실패 - Template ID {template.id}: {e}")

        if best_match and best_score >= threshold:
            group = session.query(TemplateGroup).filter(
                TemplateGroup.id == best_match.template_group_id
            ).first()
            if group:
                container = session.query(TemplateContainer).filter(
                    TemplateContainer.id == group.template_container_id
                ).first()
                results.append({
                    "filename": image.filename,
                    "matched": True,
                    "template_id": best_match.id,
                    "template_name": best_match.template_name,
                    "similarity": round(best_score, 4),
                    "template_group_name": group.template_group_name if group else None,
                    "template_container_name": container.id if container else None,
                })
            else:
                results.append({
                    "filename" : image.filename,
                    "matched" : False,
                    "similarity":round(best_score, 4) if best_score >=0 else None,
                })
    return results