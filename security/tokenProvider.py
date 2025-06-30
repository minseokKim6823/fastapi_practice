# from datetime import datetime, timedelta
# from jose import jwt
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# SECRET_KEY = os.getenv("SECRET_KEY")
# REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPORE_MINUTES")
# REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
#
# def create_token(data: dict, expires_delta: timedelta, secret_key: str):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
#
# def create_access_token(data: dict):
#     return create_token(data, timedelta(minutes=15), SECRET_KEY)
#
# def create_refresh_token(data: dict):
#     return create_token(data, timedelta(days=7), REFRESH_SECRET_KEY)
