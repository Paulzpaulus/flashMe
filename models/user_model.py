
from sqlmodel import Field, SQLModel



# index wo,wann  ?
class User(SQLModel):
    id: int | None  = Field(default= None, primary_key= True)
    name: str = Field(..., min_length=5, max_length=10)
    email: str = Field(...)
    password: str = Field(..., min_length= 5, max_length=20)




