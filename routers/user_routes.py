
from fastapi import HTTPException, APIRouter
from models.user_model import User
from service.user_CRUD import get_user, create_user, delete_user

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello You"}

# read ALL users
@router.get("/users")
async def get_user(User: User):
    if not User:
        raise HTTPException(status_code=404, detail="No Users found")
    return User


#read ONE user
@router.get("/users/{user_id}")
async def show_a_user(user_id: int):
    return {"user_id": user_id}

#create user
@router.get("/users")
async def create_user():
    pass


#edit user
@router.put("/users/{user_id}")
async def edit_user(user_id: int):
    pass

#delete user
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    pass
