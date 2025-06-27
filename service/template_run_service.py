import base64
import json
from io import BytesIO
from PIL import Image

from typing import Annotated
from fastapi import UploadFile, Form, File, Depends,HTTPException
from sqlalchemy.orm import Session
import imagehash

from model.entity.template import Template
from model.entity.template_group import TemplateGroup
from model.settings import get_session


async def upload_image_and_classify_from_db(
        threshold: Annotated[str, Form(...)],
        images_list: Annotated[list[UploadFile], File(...)],
        session: Session = Depends(get_session),
    ) -> list[dict]:
    group_objs = (
        session.query(TemplateGroup).all()
    )
    threshold_map = {
        group.template_group_name: getattr(group, "template_group_threshold", 0.7)
        for group in group_objs
    }

    try:
        incoming_data: list[dict] = json.loads(threshold)
        for item in incoming_data:
            name = item.get("template_group_name")
            value = item.get("threshold")

            if isinstance(value, (float, int)) and 0 <= value <= 1:
                threshold_map[name] = float(value)
            else:
                print(f"[!] 무시된 threshold: {name} = {value}")
    except Exception as e:
        print(f"[!] threshold JSON 무시됨: {e}")

    try:
        # 1. JSON 문자열 파싱
        threshold_data: list[dict] = json.loads(threshold)
        group_names = [item["template_group_name"] for item in threshold_data]

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"threshold JSON 파싱 오류: {e}")

    valid_groups = (
        session.query(TemplateGroup)
        .filter(TemplateGroup.template_group_name.in_(group_names))
        .all()
    )

    group_dict = {group.id: group for group in group_objs}

    # 매칭 대상 템플릿 조회
    templates = (
        session.query(Template)
        .filter(Template.template_group_id.in_([g.id for g in valid_groups]))
        .all()
    )

    results = []

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

                group = group_dict.get(template.template_group_id)
                if group is None:
                    continue
                else:
                    group_name = group.template_group_name
                    template_threshold = threshold_map.get(group_name, group.template_group_threshold)
                print(template_threshold)
                if similarity >= template_threshold and similarity > best_score:
                    print(group.template_group_threshold)

                    best_score = similarity
                    best_match = template
                    best_group = group
                    best_threshold = template_threshold

            except Exception as e:
                print(f"[!] 이미지 비교 실패 - Template ID {template.id}: {e}")
        if best_match:
            results.append({
                "filename": image.filename,
                "matched": True,
                "template_id": best_match.id,
                "template_name": best_match.template_name,
                "similarity": round(best_score, 4),
                "template_group_name": best_group.template_group_name,
                "template_group_id": best_group.id,
                "threshold": round(best_threshold, 2)
            })
        else:
            results.append({
                "filename": image.filename,
                "matched": False,
                "similarity": None,
                "threshold": None
            })

    return results