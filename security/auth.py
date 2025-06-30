# from sqlalchemy.orm import Session
# from fastapi import HTTPException
# from passlib.context import CryptContext
# from model.entity.user import User
# from security.tokenProvider import create_access_token, create_refresh_token
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def authenticate_user(user_id: str, password: str, session: Session):
#     user = session.query(User).filter(User.user_id == user_id).first()
#     if not user or not pwd_context.verify(password, user.password):
#         raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 일치하지 않습니다.")
#     return user
#
# def login_and_generate_tokens(user_id: str, password: str, session: Session):
#     user = authenticate_user(user_id, password, session)
#     access_token = create_access_token({"sub": user.user_id})
#     refresh_token = create_refresh_token({"sub": user.user_id})
#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#     }
