from typing import Optional
from sqlmodel import SQLModel, Field

# 1. Datenempfang (POST)
class UserCreate(SQLModel):
    name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    #hashed_password: str = Field(...)

# 2. Datenausgabe: Frontend  (GET)
# vererbung email, name, kein pw
class UserRead(SQLModel):
    id: int
    name: str
    email: str

# 3. Daten-Update: (PUT) -> optional sonst crash
class UserUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=10)
    email: Optional[str] = Field(default=None)
    hashed_password: Optional[str] = Field(default=None, min_length=8)

# 4. Authentifizierung (JWT)
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(SQLModel):
    username: Optional[str] = None
