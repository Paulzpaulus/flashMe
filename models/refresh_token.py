from sqlmodel import Field, SQLModel
from datetime import datetime


class RefreshToken(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    token: str = Field(unique=True)
    user_id: int = Field(foreign_key="users.id")
    expires_at: datetime
