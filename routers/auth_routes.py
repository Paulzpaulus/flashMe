

from fastapi import HTTPException, APIRouter, Response, Depends
from auth.auth import create_access_token
from config.db import get_session
from sqlmodel import Session
from service.user_CRUD import CRUD_get_user

auth = APIRouter()


@auth.post("/login")
async def login(response: Response,  session: Session = Depends(get_session)):
    print("TEST")
    user = CRUD_get_user(session = session,  id = 1)
    print(f"Hello{user}")

    if user is None:
        raise HTTPException(401)

    token = create_access_token(user.id)


    response.set_cookie(
        key="access_token",     # Name des Cookies
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",         # ?
        max_age=1800            # v30 min
    )

    return {"message": "Cookie ist gesetzt"}
