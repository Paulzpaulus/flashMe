from fastapi import HTTPException, APIRouter, Response, Depends, Body, Request
from auth.auth import create_access_token, get_current_user
from config.db import get_session
from sqlmodel import Session
from service.user_CRUD import CRUD_get_user, CRUD_create_user
from schemas.user_schema import UserCreate, UserRead

auth = APIRouter()

@auth.post("/register", response_model=UserRead)
async def register(userdata: UserCreate, session: Session = Depends(get_session)):
    password_hash = PasswordHash.recommended()
    hashed_pw = password_hash.hash(userdata.hashed_password)
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
    request: Request,
    session: Session = Depends(get_session)
):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    user = session.exec(
        Users.select().where(Users.email == email)
    ).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    password_hash = PasswordHash.recommended()
    if not password_hash.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id)
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
