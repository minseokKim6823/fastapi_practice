from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from model.settings import get_session
from security import auth
from service.login_service import get_current_user, get_new_token, oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])

class TokenData(BaseModel):
    user_id: str

@router.get("")
async def read_users_me(token: str = Depends(get_session)):
    return get_current_user(token)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return auth.login_and_generate_tokens(form_data.username, form_data.password, session)

@router.post("/refresh")
def refresh_token(refresh_token: str = Body(...)):
    get_new_token(refresh_token)