from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from model.dto.groupDTO import createGroup, modifyGroup
from model.entity.template_container import TemplateContainer
from model.entity.template_group import TemplateGroup


async def createTemplateGroup(
        group: createGroup,
        session: Session
    ):
    threshold = group.template_group_threshold if group.template_group_threshold is not None else 0.7
    db_group = TemplateGroup(
        template_group_name=group.template_group_name,
        template_container_id=group.template_container_id,
        template_group_threshold=threshold
    )

    session.add(db_group)
    session.commit()
    session.refresh(db_group)
    return {"id": db_group.id}

def updateTemplateGroup(
        id: int,
        updated_data: modifyGroup,
        session: Session
    ):
    # existing = session.query(TemplateGroup).filter(TemplateGroup.template_group_name == updated_data.template_group_name).first()
    # if existing:
    #     return {"error": f"이미 존재하는 template_group_name: {updated_data.template_group_name}"}
    # isExist = session.query(TemplateContainer).filter(TemplateContainer.id == updated_data.template_container_id).first()
    # if not isExist:
    #     return "해당 container를 찾을 수 없습니다."
    # else:
        threshold = updated_data.template_group_threshold if updated_data.template_group_threshold is not None else 0.7
        group = session.query(TemplateGroup).filter(TemplateGroup.id == id).first()
        group.template_group_name = updated_data.template_group_name
        group.template_group_threshold = threshold
        group.template_container_id = updated_data.template_container_id
        session.commit()
        session.refresh(group)
        return {"id": group.id}

def findAllGroups(session: Session, page: int = 1, limit: int = 10):
    if page <= 0:
        return {"error": "페이지는 1부터 시작합니다."}
    else:
        offset = (page - 1) * 10
        total = session.query(TemplateGroup).count()
        allPosts = (
            session.query(TemplateGroup)
            .offset(offset)
            .limit(limit)
            .all())
        containers = session.query(TemplateContainer).all()
        container_map = {c.id: c.template_container_name for c in containers}
        return {
            "total": total,
            "page": page,

            "posts": [
                {
                    "template_group_id": post.id,
                    "template_group": post.template_group_name,
                    "template_container_id":post.template_container_id,
                    "template_container_name": container_map.get(post.template_container_id, None),
                    "template_group_threshold":post.template_group_threshold
                }
                for post in allPosts
            ]
        }

def deleteById(id: int, session: Session):
    group = session.query(TemplateGroup).filter(TemplateGroup.id == id).first()

    if not group:
        raise HTTPException(status_code=400, detail="해당 그룹을 찾을 수 없습니다.")
    try:
        session.delete(group)
        session.commit()
        return {"id": group.id}
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="삭제 실패: 해당 그룹에 연결된 템플릿이 존재합니다.")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"삭제 실패: {str(e)}")

