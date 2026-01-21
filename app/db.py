from pydantic import BaseModel, Field
from typing import Annotated


class Userbase(BaseModel):
    user_id = int
    user_name = str
    user_email = str


class UserRead(BaseException):


