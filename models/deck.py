from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class Deck(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(
        min_length=1,
        max_length=100,

    )

    description: str | None = Field(
        default=None,
        max_length=500,

    )

    owner_id: int = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,

    )

    is_public: bool = Field(
        default=False,

    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),

    )
