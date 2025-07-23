import json
from typing import Union

import imagehash
from io import BytesIO
from PIL import Image
from fastapi import UploadFile

def calc_hash_similarity(uploaded_hash, template_image, hash_size=128) -> float:
    template_hash = imagehash.average_hash(template_image, hash_size=hash_size)
    diff = uploaded_hash - template_hash
    return 1 - (diff / (hash_size**2))


def get_image_size_from_uploadfile(
        upload_file: Union[UploadFile, bytes]
    ) -> tuple[int, int]:
    if isinstance(upload_file, (bytes, bytearray)):
        img = Image.open(BytesIO(upload_file))
    else:
        upload_file.file.seek(0)
        contents = upload_file.file.read()
        img = Image.open(BytesIO(contents))
    return img.width, img.height

def normalize_boxes(boxes, width, height):
    if not boxes:
        return []
    return [
        [x / width, y / height, w / width, h / height]
        for x, y, w, h in boxes
    ]
def re_normalize_boxes(
    bbox_dict: dict[str, list[float]],
    width: int,
    height: int
) -> dict[str, tuple[int, int, int, int]]:
    normalized: dict[str, tuple[int, int, int, int]] = {}
    for key, coords in bbox_dict.items():
        if (
            not isinstance(coords, (list, tuple)) or
            len(coords) != 4
        ):
            continue

        x_rel, y_rel, w_rel, h_rel = coords
        x_px = int(x_rel * width)
        y_px = int(y_rel * height)
        w_px = int(w_rel * width)
        h_px = int(h_rel * height)

        normalized[key] = (x_px, y_px, w_px, h_px)
    return normalized

def parse_and_normalize_fields(field_str, width, height):
    fields = json.loads(field_str) if field_str else []
    if width and height:
        for f in fields:
            if "bbox" in f:
                x, y, w, h = f["bbox"]
                f["bbox"] = [x / width, y / height, w / width, h / height]
    return json.dumps(fields, ensure_ascii=False)

def re_parse_and_normalize_fields(
        field_str,
        width,
        height):

    if width and height:
        for f in field_str:
            if "bbox" in f:
                x, y, w, h = f["bbox"]
                f["bbox"] = [int(x * width), int(y * height), int(w * width), int(h * height)]
    return json.dumps(field_str, ensure_ascii=False)