from fastapi import HTTPException

from sqlalchemy.orm import Session

from model.entity.template_container import TemplateContainer


async def createTemplateContainer(
        template_container_name: str,
        session: Session
    ):
    container = TemplateContainer(
        template_container_name=template_container_name
    )
    session.add(container)
    session.commit()
    return {"id": container.id}

def updateTemplateContainer(
        id: int,
        template_container_name:str,
        session: Session
    ):
    container = session.query(TemplateContainer).filter(TemplateContainer.id == id).first()
    # 있는지
    if not container:
        raise HTTPException(status_code=400, detail="해당 컨테이너를 찾을 수 없습니다.")


    # 중복방지
    existing = session.query(TemplateContainer).filter(TemplateContainer.template_container_name == template_container_name, TemplateContainer.id != id).first()
    if existing:
        raise HTTPException(status_code=400, detail= f"다른 게시물에서 이미 사용 중인 template_container_name 입니다 : {template_container_name}")

    container.template_container_name = template_container_name

    session.commit()
    session.refresh(container)
    return {"id": container.id}

def findAllContainers(session: Session, page: int = 1, limit: int = 10):
    if page <= 0:
        return {"error": "페이지는 1부터 시작합니다."}
    else:
        offset = (page - 1) * 10
        total = session.query(TemplateContainer).count()
        allPosts = session.query(TemplateContainer).offset(offset).limit(limit).all()
        return {
            "total": total,
            "page": page,
            "posts": [
                {"template_containers": post.template_container_name}
                for post in allPosts
            ]
        }

def deleteById(id: int, session: Session):
    container = session.query(TemplateContainer).filter(TemplateContainer.id == id).first()
    if container:
        session.delete(container)
        session.commit()
        return {"id": container.id}
    else:
        raise HTTPException(status_code = 400, detail = "해당 컨테이너를 찾을 수 없습니다.")