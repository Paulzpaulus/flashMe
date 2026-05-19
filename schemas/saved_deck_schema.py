from sqlmodel import SQLModel
from datetime import datetime


class SavedDeckCreate(SQLModel):
    deck_id: int


class SavedDeckRead(SQLModel):
    user_id: int
    deck_id: int
    saved_at: datetime
