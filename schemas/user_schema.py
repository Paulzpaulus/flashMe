from typing import Optional
from sqlmodel import SQLModel, Field
from models.user import User

# 1. Datenempfang (POST)
class UserCreate(User):
    hashed_password: str = Field(min_length=8, max_length=50)

# 2. Datenausgabe: Frontend  (GET)
# vererbung email, name, kein pw
class UserRead(User):
    pass

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
