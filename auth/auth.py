import os # type: ignore
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from pwdlib import PasswordHash
from passlib.context import CryptContext
from sqlmodel import Session
from config.db import get_session
from models.user import Users


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(user_id: int) -> str:
    from datetime import timezone
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: dict[str, str | int | float] = {"sub": str(user_id), "exp": expire.timestamp()}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No Cookie found")
    return token


def get_current_user(request: Request, session: Session = Depends(get_session)) -> Users:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authorised")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user = session.get(Users, user_id)
        if not user:
            raise HTTPException(status_code=401)
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")





def get_pw(): # type str?
    password_hash = PasswordHash.recommended()
    DUMMY_HASH = password_hash.hash("dummypassword")
    return password_hash, DUMMY_HASH

"""def verify_password(plain_password, hashed_password) -> str:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)"""
