# from sqlalchemy.orm import Session
# from model.dto.userDTO import createAccount, modifyUserInfo
# from model.entity.user import User
# from passlib.context import CryptContext
# from fastapi import HTTPException, status
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def createAccount(user: createAccount , session:Session):
#     existing_user = session.query(User).filter(User.user_id == user.user_id).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="이미 등록된 아이디입니다.")
#
#     hashed_password = pwd_context.hash(user.password)
#     db_user = User(
#         user_id=user.user_id,
#         password=hashed_password
#     )
#
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)
#     return "회원 가입 성공"
#
# def modify(id: int, updated_data: modifyUserInfo, session: Session):
#     user =session.query(User).filter(User.id == id).first()
#     user.username = updated_data.username
#     user.image = updated_data.image
#     session.commit()
#     session.refresh(user)
#     return user