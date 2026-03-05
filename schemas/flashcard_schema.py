from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class FlashcardCreate(SQLModel):
    # Notice: no deck_id here — deck comes from the URL path /decks/{deck_id}/cards
    # This is cleaner and prevents users from assigning cards to foreign decks.
    front: str = Field(min_length=1, max_length=1000)
    back: str = Field(min_length=1, max_length=1000)


class FlashcardRead(SQLModel):
    id: int
    front: str
    back: str
    deck_id: int
    created_at: datetime


class FlashcardUpdate(SQLModel):
    front: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    back: Optional[str] = Field(default=None, min_length=1, max_length=1000)
