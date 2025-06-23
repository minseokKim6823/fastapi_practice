from fastapi import APIRouter, Depends, Body, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from security.JWTSettings import REFRESH_SECRET_KEY, ALGORITHM, SECRET_KEY
from security.tokenProvider import create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class TokenData(BaseModel):
    user_id: str

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    print(token_data)
    return {"user_id": token_data.user_id}

def get_new_token(refresh_token):
    payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    # 유효성 검사 등
    new_access_token = create_access_token({"sub": user_id})
    return {"access_token": new_access_token}