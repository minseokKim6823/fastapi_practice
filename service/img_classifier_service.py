from typing import List
from PIL import Image
from io import BytesIO
import base64
import imagehash
from sqlalchemy.orm import Session

from model.entity.template import Template
from model.entity.template_group import TemplateGroup
from utils.image_utils import calc_hash_similarity
from utils.threshold_parser import parse_threshold_data


class TemplateClassifier:
    def __init__(self, session: Session):
        self.session = session

    def get_templates_and_groups(self, group_names: List[str]):
        valid_groups = (
            self.session.query(TemplateGroup)
            .filter(TemplateGroup.template_group_name.in_(group_names))
            .all()
        )
        group_dict = {group.id: group for group in valid_groups}

        templates = (
            self.session.query(Template)
            .filter(Template.template_group_id.in_(group_dict.keys()))
            .all()
        )

        return templates, group_dict

    def classify_image(self, image_bytes: bytes, templates: List[Template], group_dict, threshold_map: dict):
        try:
            uploaded_image = Image.open(BytesIO(image_bytes))
            uploaded_hash = imagehash.average_hash(uploaded_image, hash_size=128)
        except Exception as e:
            return {"error": f"이미지를 열 수 없습니다: {e}"}

        best_match = None
        best_score = -1.0
        best_group = None
        best_threshold = 0.7

        for template in templates:
            try:
                decoded = base64.b64decode(template.image)
                template_image = Image.open(BytesIO(decoded))
                similarity = calc_hash_similarity(uploaded_hash, template_image)

                group = group_dict.get(template.template_group_id)
                if not group:
                    continue

                group_name = group.template_group_name
                threshold = threshold_map.get(group_name, group.template_group_threshold)

                if similarity >= threshold and similarity > best_score:
                    best_score = similarity
                    best_match = template
                    best_group = group
                    best_threshold = threshold

            except Exception as e:
                print(f"[!] 이미지 비교 실패 - Template ID {template.id}: {e}")

        if best_match:
            return {
                "matched": True,
                "template_id": best_match.id,
                "template_name": best_match.template_name,
                "similarity": round(best_score, 4),
                "template_group_name": best_group.template_group_name,
                "template_group_id": best_group.id,
                "threshold": round(best_threshold, 2),
            }

        return {"matched": False, "similarity": None, "threshold": None}
