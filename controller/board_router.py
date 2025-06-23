import base64

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response
from sqlalchemy.orm import Session

from service import board_service
from model.dto.boardDTO import BoardPartialRead, BoardListResponse
from model.settings import get_session
# from service.login_service import get_current_user

router = APIRouter(prefix="/board", tags=["board"])

@router.post("")
async def create(
        name: str = Form(...),
        image: UploadFile = File(...),
        field: str = Form(...),
        group_id: int = Form(...),
        session: Session = Depends(get_session)
    ):
    return await board_service.createBoard(name, image, field, group_id, session)

@router.put("{id}")
async def update(
        id: int,
        name: str = Form(...),
        image: UploadFile = File(...),
        field: str = Form(...),
        group_id: int = Form(...),
        session: Session = Depends(get_session)
    ):
    return await board_service.updatePost(id, name, image, field,group_id, session)


@router.get("/image/{id}")
def readImageById(id: int, session: Session = Depends(get_session)):
    post = board_service.findImageById(id, session)
    try:
        image_data = base64.b64decode(post.image)
    except Exception:
        return {"error": "이미지 디코딩 실패"}

    return Response(content=image_data, media_type=post.content_type)

@router.get("/fields/{id}", response_model=BoardPartialRead)
def readFieldsById(id: int, session: Session = Depends(get_session)):
    post = board_service.findFieldsById(id, session)
    if not post:
        return {"error": "게시물을 찾을 수 없습니다"}
    return post


@router.get("", response_model=BoardListResponse)
def readAll(session: Session = Depends(get_session), offset: int = 1, limit: int = 10):
    return board_service.findAll(session, offset, limit)

@router.delete("{id}")
def delete(id: int,  session: Session = Depends(get_session)):
    return board_service.deleteById(id, session)

