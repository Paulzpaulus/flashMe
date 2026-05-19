from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class CardProgressRead(SQLModel):
    user_id: int
    card_id: int
    ease_factor: float
    interval: int
    repetitions: int
    next_review: datetime


class CardProgressUpdate(SQLModel):
    ease_factor: Optional[float] = None
    interval: Optional[int] = None
    repetitions: Optional[int] = None
    next_review: Optional[datetime] = Field(default=None)
