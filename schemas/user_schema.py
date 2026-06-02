from typing import Optional, Annotated
from pydantic import AfterValidator
from sqlmodel import SQLModel, Field


def _check_email(v: str) -> str:
    if "@" not in v:
        raise ValueError("Invalid email address")
    local, _, domain = v.partition("@")
    if (
        not local
        or not domain
        or "." not in domain
        or domain.startswith(".")
        or domain.endswith(".")
    ):
        raise ValueError("Invalid email address")
    return v.lower()


Email = Annotated[str, AfterValidator(_check_email)]


# 1. Datenempfang (POST)
class UserCreate(SQLModel):
    name: str = Field(...)
    email: Email
    password: str = Field(...)


class UserAdminCreate(UserCreate):
    is_admin: bool = False


# 2. Datenausgabe: Frontend  (GET)
class UserRead(SQLModel):
    id: int
    name: str
    email: str
    is_admin: bool


# 3. Daten-Update: (PUT) -> optional sonst crash
# password kommt als Klartext rein, wird im Router gehasht
class UserUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=10)
    email: Optional[Email] = None
    password: Optional[str] = Field(default=None, min_length=8)


# 4. Authentifizierung (JWT)
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    username: Optional[str] = None
