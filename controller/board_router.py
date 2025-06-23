import base64

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response
from sqlalchemy.orm import Session

from service import board_service
from model.dto.boardDTO import boardCreate
from model.settings import get_session
from service.login_service import get_current_user

router = APIRouter(prefix="/board", tags=["board"])

@router.post("")
async def create(
        name: str = Form(...),
        writer: str = Form(...),
        image: UploadFile = File(...),
        session: Session = Depends(get_session)
    ):
    return await board_service.createBoard(name, writer, image, session)


@router.get("/{id}")
def readById(id: int, session: Session = Depends(get_session)):
    post = board_service.findById(id, session)
    try:
        image_data = base64.b64decode(post.image)
    except Exception:
        return {"error": "이미지 디코딩 실패"}

    return Response(content=image_data, media_type=post.content_type)


@router.get("")
def readAll( session: Session = Depends(get_session), offset: int = 0, limit: int = 10):
    return board_service.findAll(session, offset, limit)

@router.delete("{id}")
def delete(id: int,  session: Session = Depends(get_session)):
    return board_service.deleteById(id, session)

@router.put("{id}")
def update(id: int, updated_data: boardCreate,  session: Session = Depends(get_session)):
    return board_service.updatePost(id, updated_data, session)
