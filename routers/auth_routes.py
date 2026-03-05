from fastapi import HTTPException, APIRouter, Response, Depends, Request
from auth.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password
)
from config.db import get_session
from sqlmodel import Session, select
from service.user_CRUD import CRUD_create_user
from schemas.user_schema import UserCreate, UserRead
from schemas.login_schema import LoginRequest
from models.user import Users
from typing import cast

auth = APIRouter()

@auth.post("/register", response_model=UserRead)
async def register(userdata: UserCreate, session: Session = Depends(get_session)):
    hashed_pw = hash_password(userdata.password)
    user = Users(
        name=userdata.name,
        email=userdata.email,
        hashed_password=hashed_pw
    )
    created_user = CRUD_create_user(session, user)
    return created_user


@auth.post("/login")
async def login(
    response: Response,
    credentials: LoginRequest,
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(Users).where(Users.email == credentials.email)
    ).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = create_access_token(cast(int, user.id))
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=1800
    )
    return {"message": "Login successful"}


@auth.get("/me", response_model=UserRead)
async def read_me(user: Users = Depends(get_current_user)):
    return user
