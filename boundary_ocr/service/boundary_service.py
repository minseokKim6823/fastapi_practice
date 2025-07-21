from sqlalchemy.orm import Session
from boundary_ocr.entity.boundary import Boundary
from boundary_ocr.utils.images_size import get_image_size_from_base64
from model.entity.template import Template


async def createBoundary(
        boundary_field: list[float],
        template_id: int,
        session: Session
):
    template: Template = session.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise ValueError("Template not found")

    img_width, img_height = get_image_size_from_base64(template.image)

    x_ratio = boundary_field[0] / img_width
    y_ratio = boundary_field[1] / img_height
    w_ratio = boundary_field[2] / img_width
    h_ratio = boundary_field[3] / img_height

    boundary_obj = Boundary(
        boundary_field=[x_ratio, y_ratio, w_ratio, h_ratio],
        template_id = template_id
    )

    session.add(boundary_obj)
    session.commit()
    session.refresh(boundary_obj)

    return {"id": boundary_obj.id}
