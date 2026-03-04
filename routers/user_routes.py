
from fastapi import HTTPException, APIRouter, Depends
from sqlmodel import Session
from models.user import Users
from service.user_CRUD import CRUD_get_user, CRUD_create_user, CRUD_delete_user, CRUD_update_user, CRUD_get_all_users
from config.db import get_session



user_routes = APIRouter()

@user_routes.get("/")
async def root():
    return {"message": "Hello You"}

# read ALL users
@user_routes.get("/users")
async def get_users(user_id: int, session: Session = Depends(get_session)):
    users = CRUD_get_all_users(session)
    if not users:
        raise HTTPException(status_code=404, detail="No Users found")
    return users # should be list


#read ONE user
@user_routes.get("/users/{user_id}")
async def show_a_user(user_id: int, session: Session = Depends(get_session)):
    user = CRUD_get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#create user
@user_routes.post("/users")
async def create_user(user: Users, session: Session = Depends(get_session)):
    created_user = CRUD_create_user(session, user)
    print(f"{created_user} created.")
    return created_user



#edit user
@user_routes.put("/users/{user_id}")
async def edit_user(user_id: int, session: Session = Depends(get_session)):
    CRUD_update_user(session, user_id)
    print("user updated")

#delete user
@user_routes.delete("/users/{user_id}")
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    CRUD_delete_user(session, user_id)
    print(f"User with id {user_id} deleted")


