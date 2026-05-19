from fastapi import HTTPException, APIRouter, Response, Depends, Request
from auth.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
    create_refresh_token,
)
from config.db import get_session
from sqlmodel import Session, select
from service.user_CRUD import CRUD_create_user
from schemas.user_schema import UserCreate, UserRead
from schemas.login_schema import LoginRequest
from models.refresh_token import RefreshToken
from models.user import Users
from typing import cast
from datetime import datetime, timezone

auth = APIRouter()


@auth.post("/register", response_model=UserRead)
async def register(userdata: UserCreate, session: Session = Depends(get_session)):
    hashed_pw = hash_password(userdata.password)
    user = Users(name=userdata.name, email=userdata.email, hashed_password=hashed_pw)
    created_user = CRUD_create_user(session, user)
    return created_user


@auth.post("/login")
async def login(
    response: Response,
    credentials: LoginRequest,
    session: Session = Depends(get_session),
):
    user = session.exec(select(Users).where(Users.email == credentials.email)).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    access_token = create_access_token(cast(int, user.id))
    refresh_token = create_refresh_token(cast(int, user.id), session)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=1800,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )
    return {"message": "Login successful"}


@auth.post("/logout")
async def logout_user(
    request: Request, response: Response, session: Session = Depends(get_session)
):
    token = request.cookies.get("refresh_token")
    if token:
        db_token = session.exec(
            select(RefreshToken).where(RefreshToken.token == token)
        ).first()
        if db_token:
            session.delete(db_token)
            session.commit()
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "Logged out"}


@auth.post("/refresh")
async def refresh_auth(
    request: Request, response: Response, session: Session = Depends(get_session)
):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token")

    db_token = session.exec(
        select(RefreshToken).where(RefreshToken.token == token)
    ).first()
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired")

    new_access_token = create_access_token(db_token.user_id)
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=1800,
    )
    new_refresh_token = create_refresh_token(db_token.user_id, session)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )
    return {"message": "Token refreshed"}


@auth.get("/me", response_model=UserRead)
async def read_me(user: Users = Depends(get_current_user)):
    return user
