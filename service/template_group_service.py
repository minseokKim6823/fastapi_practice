from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from model.dto.groupDTO import createGroup, modifyGroup
from model.entity.template_group import TemplateGroup


async def createTemplateGroup(
        group: createGroup,
        session: Session
    ):
    # existing = session.query(TemplateGroup).filter(TemplateGroup.template_group_name == group.template_group_name).first()
    # if existing:
    #     return {"error": f"이미 존재하는 template_group_name: {group.template_group_name}"}


    threshold = group.template_group_threshold if group.template_group_threshold is not None else 0.7

    db_group = TemplateGroup(
        template_group_name=group.template_group_name,
        template_container_id=group.template_container_id,
        template_group_threshold=threshold
    )

    session.add(db_group)
    session.commit()
    session.refresh(db_group)
    return "저장 완료 "

def updateTemplateGroup(
        id: int,
        updated_data: modifyGroup,
        session: Session
    ):
    # existing = session.query(TemplateGroup).filter(TemplateGroup.template_group_name == updated_data.template_group_name).first()
    # if existing:
    #     return {"error": f"이미 존재하는 template_group_name: {updated_data.template_group_name}"}
    threshold = updated_data.template_group_threshold if updated_data.template_group_threshold is not None else 0.7
    group = session.query(TemplateGroup).filter(TemplateGroup.id == id).first()
    group.template_group_name = updated_data.template_group_name
    group.template_group_threshold = threshold
    group.template_container_id = updated_data.template_container_id
    session.commit()
    session.refresh(group)
    return "수정완료"

def findAllGroups(session: Session, page: int = 1, limit: int = 10):
    if page <= 0:
        return {"error": "페이지는 1부터 시작합니다."}
    else:
        offset = (page - 1) * 10
        total = session.query(TemplateGroup).count()
        allPosts = session.query(TemplateGroup).offset(offset).limit(limit).all()
        return {
            "total": total,
            "page": page,
            "posts": [
                {
                    "template_group_id": post.id,
                    "template_group": post.template_group_name,
                    "template_container_id":post.template_container_id,
                    "template_group_threshold":post.template_group_threshold
                }
                for post in allPosts
            ]
        }

def deleteById(id: int, session: Session):
    post = session.query(TemplateGroup).filter(TemplateGroup.id == id).first()

    if not post:
        return "해당 그룹을 찾을 수 없습니다."

    try:
        session.delete(post)
        session.commit()
        return f"{id}번 그룹이 삭제되었습니다."
    except IntegrityError as e:
        session.rollback()
        return f"삭제 실패: 해당 그룹에 연결된 템플릿이 존재합니다. ({str(e.orig)})"
    except Exception as e:
        session.rollback()
        return f"알 수 없는 오류로 삭제에 실패했습니다: {str(e)}"