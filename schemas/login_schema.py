
from sqlmodel import SQLModel, Field

class LoginRequest(SQLModel):
    email: str
    password: str
