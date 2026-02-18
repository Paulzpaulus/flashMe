from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from jwt import encode
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlmodel import SQLModel
from datetime import datetime, timedelta



SECRET_KEY = "d0dc2f7e8f9634f02c3c3140996f7eda76363ac4f7489aea44e21e1907cc83d4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: str | None = None

def fake_decode_token(token): # type: ignore
    return User(
        name=token + "fakedecoded", email="paula@test.com"
        ) # type: ignore

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user



def create_token(user_id: str):
    payload = { # type: ignore
        "sub": user_id,
        "exp": datetime.now() + timedelta(minutes=30) # type: ignore
    }

    token = encode(payload, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return token
