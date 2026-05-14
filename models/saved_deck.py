from sqlmodel import Field, SQLModel
from datetime import timezone, datetime


class SavedDeck(SQLModel, table=True):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    deck_id: int = Field(foreign_key="deck.id", primary_key=True)
    saved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
