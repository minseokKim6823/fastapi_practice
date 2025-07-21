from boundary_ocr.service import boundary_service
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model.settings import get_session

router = APIRouter(prefix="", tags=["boundary"])

@router.post("/{template_id}/boundary")
async def boundary(
        boundary_field: list[float],
        template_id: int,
        session: Session = Depends(get_session)):
    return await boundary_service.createBoundary(boundary_field, template_id, session)