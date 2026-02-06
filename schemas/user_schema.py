from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    user_password: str = Field(min_length= 5, max_length= 50)


class UserRead(BaseModel):
    user_id: int
