from sqlmodel import Field, SQLModel
from datetime import timezone, datetime

class Flashcard(SQLModel, table = True):

    id: int | None = Field(default=None, primary_key=True)

    deck_id: int = Field(
        foreign_key="deck.id",
        nullable=False,
        index=True
    )

    front: str = Field(
        min_length=1,
        max_length= 1000,
    )

    back: str = Field(
        min_length=1,
        max_length= 1000
    )



    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
