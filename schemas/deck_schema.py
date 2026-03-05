from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class DeckCreate(SQLModel):
    # Notice: no owner_id here — we get that from the auth cookie, not from
    # the user's request body. This prevents someone faking another user's ID.
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    is_public: bool = Field(default=False)


class DeckRead(SQLModel):
    id: int
    title: str
    description: Optional[str]
    owner_id: int
    is_public: bool
    created_at: datetime


class DeckUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    is_public: Optional[bool] = None
