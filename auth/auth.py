from fastapi import Request, HTTPException, APIRouter, Response, Depends
from sqlmodel import Session
        # db connection
from models.user import User                  #db model
from schemas.user_schema import UserCreate         # input val
from config.db import get_session            # db
from jwt import decode
from service.user_CRUD import CRUD_get_user

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

def create_access_token(user_id: int) -> str:
    payload = { # type: ignore
        "sub": user_id,
        "exp": datetime.now() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES) # type: ignore
    }

    token = encode(payload, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return token # type: ignore

@router.post("/login") # type: ignore
async def login(data: Response,  session: Session = Depends(get_session)):
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


def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Kein Cookie gefunden")
    return token


def get_current_user(request: Request, session: Session = Depends(get_session)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Nicht autorisiert")

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=401)
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token ungültig")


""""

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




"""
