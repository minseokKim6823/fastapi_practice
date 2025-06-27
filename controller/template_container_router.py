from model.dto.containerDTO import createContainer, modifyContainer
from service import template_container_service
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session


from model.settings import get_session

router = APIRouter(prefix="/container", tags=["container"])

@router.post("")
async def create(
        dto : createContainer,
        session: Session = Depends(get_session)
    ):
    return await template_container_service.createTemplateContainer(dto.template_container_name, session)

@router.put("/{id}")
def update(
        id: int,
        dto : modifyContainer,
        session: Session = Depends(get_session)
    ):
    return template_container_service.updateTemplateContainer(id, dto.template_container_name, session)

@router.get("")
def read(session: Session = Depends(get_session), offset: int = 1, limit: int = 10):
    return template_container_service.findAllContainers(session, offset, limit)

@router.delete("/{id}")
def delete(
        id: int,session: Session = Depends(get_session)
    ):
    return template_container_service.deleteById(id, session)


