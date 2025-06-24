from sqlalchemy.orm import Session

from model.entity.template_group import TemplateGroup


async def createTemplateGroup(
        template_group_name: str,
        session: Session
    ):

    existing = session.query(TemplateGroup).filter(TemplateGroup.template_group_name == template_group_name).first()
    if existing:
        return {"error": f"이미 존재하는 template_group_name: {template_group_name}"}

    db_board = TemplateGroup(
        template_group_name=template_group_name,
        # field=parsed_field
    )
    session.add(db_board)
    session.commit()
    return "저장완료"