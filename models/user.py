from sqlmodel import Field, SQLModel
from typing import Optional


class UserBase(SQLModel):
    name: str = Field(min_length=3, max_length=10, index=True)
    email: str = Field(unique=True, index=True, nullable=False)



class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)  #niemals echtes pw



