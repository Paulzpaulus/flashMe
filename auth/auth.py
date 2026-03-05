import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from pwdlib import PasswordHash
from sqlmodel import Session
from config.db import get_session
from models.user import Users


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def hash_password(password: str) -> str:
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, hashed)

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: dict[str, str | int | float] = {"sub": str(user_id), "exp": expire.timestamp()}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No Cookie found")
    return token


def get_current_user(request: Request, session: Session = Depends(get_session)) -> Users:
    token = get_token_from_cookie(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(status_code=401, detail="Token missing user id")
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user



