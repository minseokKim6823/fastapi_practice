from sqlalchemy.orm import Session

from model.entity.template_container import TemplateContainer


async def createTemplateContainer(
        template_container_name: str,
        session: Session
    ):
    existing = session.query(TemplateContainer).filter(TemplateContainer.template_container_name == template_container_name).first()
    if existing:
        return {"error": f"이미 존재하는 template_container_name: {template_container_name}"}

    db_board = TemplateContainer(
        template_container_name=template_container_name
    )
    session.add(db_board)
    session.commit()
    return "저장 완료 "

def updateTemplateContainer(
        id: int,
        template_container_name:str,
        session: Session
    ):
    post = session.query(TemplateContainer).filter(TemplateContainer.id == id).first()
    # 있는지
    if not post:
        return "해당 컨테이너를 찾을 수 없습니다."

    # 중복방지
    existing = session.query(TemplateContainer).filter(TemplateContainer.template_container_name == template_container_name, TemplateContainer.id != id).first()
    if existing:
        return {"error": f"다른 게시물에서 이미 사용 중인 template_container_name 입니다 : {template_container_name}"}

    post.template_container_name = template_container_name

    session.commit()
    session.refresh(post)
    return "수정완료"

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
    post = session.query(TemplateContainer).filter(TemplateContainer.id == id).first()
    if post:
        session.delete(post)
        session.commit()
        return f"{id}번 컨테이너가 삭제되었습니다."
    else:
        return "해당 컨테이너를 찾을 수 없습니다."