from typing import Optional
from sqlmodel import SQLModel, Field

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


# 1. Datenempfang (POST)
class UserCreate(SQLModel):
    name: str = Field(...)
    email: str = Field(pattern=EMAIL_REGEX)
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
    email: Optional[str] = Field(default=None, pattern=EMAIL_REGEX)
    password: Optional[str] = Field(default=None, min_length=8)


# 4. Authentifizierung (JWT)
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    username: Optional[str] = None
