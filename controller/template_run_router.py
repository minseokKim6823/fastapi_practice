# from fastapi import APIRouter, UploadFile, File, Depends, Form
# from fastapi.responses import Response
# from typing import Annotated
# from requests import Session
#
# from model.settings import get_session
# from service import template_run_service
# from service.template_run_service import upload_image_and_classify_from_db
#
# router=APIRouter(prefix="/run",tags=["run_template"])
#
# # @router.post("/upload")
# # async def upload(image: Optional[UploadFile] = File(None)):
# #     if image is None:
# #         return Response(content=b"No image uploaded", status_code=400)
# #
# #     image_data = await template_run_service.uploadImg(image)
# #     image_data = base64.b64decode(image_data)
# #
# #     return Response(content=image_data, media_type="image/jpeg")
#
#
# @router.post("/images/match")
# async def run_match_images(
#         threshold: Annotated[str, Form(...)],
#         images_list: Annotated[list[UploadFile], File(...)],
#         session: Session = Depends(get_session)
#         ):
#     result = await upload_image_and_classify_from_db(threshold, images_list, session)
#     return result
from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException
from typing import Annotated, List

from model.entity.template import Template
from model.entity.template_group import TemplateGroup
from model.settings import get_session
from service.img_classifier_service import TemplateClassifier
from utils.threshold_parser import parse_threshold_data

router = APIRouter()


@router.post("/classify")
async def upload_image_and_classify_from_db(
    threshold: Annotated[str, Form(...)],
    images_list: Annotated[List[UploadFile], File(...)],
    session=Depends(get_session),
):
    try:
        threshold_map, group_names = parse_threshold_data(threshold)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    classifier = TemplateClassifier(session)
    templates, group_dict = classifier.get_templates_and_groups(group_names)

    results = []
    for image in images_list:
        uploaded_bytes = await image.read()
        result = classifier.classify_image(uploaded_bytes, templates, group_dict, threshold_map)
        result["filename"] = image.filename
        results.append(result)

    return results


@router.post("/{id}/classify")
async def upload_image_and_classify_from_db_by_container_id(
        id: int,
        images_list: Annotated[List[UploadFile], File(...)],
        session=Depends(get_session),
):

    classifier = TemplateClassifier(session)


    templates = (
        session.query(Template)
        .join(TemplateGroup, Template.template_group_id == TemplateGroup.id)
        .filter(TemplateGroup.template_container_id == id)
        .all()
    )


    results = []
    for image in images_list:
        uploaded_bytes = await image.read()
        result = classifier.classify_image_container_version(id, uploaded_bytes, templates)
        result["filename"] = image.filename
        results.append(result)

    return results