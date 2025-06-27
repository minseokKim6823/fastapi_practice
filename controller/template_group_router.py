from model.dto.groupDTO import createGroup, modifyGroup
from service import template_group_service
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from model.settings import get_session

router = APIRouter(prefix="/group", tags=["group"])

@router.post("")
async def create(
        template_group: createGroup,
        session: Session = Depends(get_session)
    ):
    return await template_group_service.createTemplateGroup(template_group, session)

@router.put("/{id}")
def update(
        id: int,
        template_group: modifyGroup,
        session: Session = Depends(get_session)
    ):
    return template_group_service.updateTemplateGroup(id, template_group, session)

@router.get("")
def read(session: Session = Depends(get_session), offset: int = 1, limit: int = 10):
    return template_group_service.findAllGroups(session, offset, limit)


@router.delete("/{id}")
def delete(
        id: int,session: Session = Depends(get_session)
    ):
    return template_group_service.deleteById(id, session)


