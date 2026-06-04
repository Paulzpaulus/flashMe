from typing import Optional
from sqlmodel import SQLModel, Field

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class UserCreate(SQLModel):
    name: str = Field(...)
    email: str = Field(regex=EMAIL_REGEX)
    password: str = Field(...)


class UserAdminCreate(UserCreate):
    is_admin: bool = False


class UserRead(SQLModel):
    id: int
    name: str
    email: str
    is_admin: bool


class UserUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=10)
    email: Optional[str] = Field(default=None, regex=EMAIL_REGEX)
    password: Optional[str] = Field(default=None, min_length=8)


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    username: Optional[str] = None
