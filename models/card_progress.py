from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class CardProgress(SQLModel, table=True):
    user_id: int = Field(primary_key=True, foreign_key="users.id")
    card_id: int = Field(primary_key=True, foreign_key="flashcard.id")
    ease_factor: float = Field(default=2.5)
    interval: int = Field(default=1)
    repetitions: int = Field(default=0)
    next_review: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
