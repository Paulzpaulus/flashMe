
from fastapi import HTTPException, APIRouter, Depends
from sqlmodel import Session
from models.user import User
from service.user_CRUD import CRUD_get_user, CRUD_create_user, CRUD_delete_user, CRUD_update_user, CRUD_get_all_users
from config.db import get_session



router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello You"}

# read ALL users
@router.get("/users")
async def get_users(user_id: int, session: Session = Depends(get_session)):
    users = CRUD_get_all_users(session)
    if not users:
        raise HTTPException(status_code=404, detail="No Users found")
    return users # should be list


#read ONE user
@router.get("/users/{user_id}")
async def show_a_user(user_id: int, session: Session = Depends(get_session)):
    user = CRUD_get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#create user
@router.post("/users")
async def create_user(user: User, session: Session = Depends(get_session)):
    created_user = CRUD_create_user(session, user)
    print(f"{created_user} created.")
    return created_user



#edit user
@router.put("/users/{user_id}")
async def edit_user(user_id: int, session: Session = Depends(get_session)):
    CRUD_update_user(session, user_id)
    print("user updated")

#delete user
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    CRUD_delete_user(session, user_id)
    print(f"User with id {user_id} deleted")


#user login
@router.get("/login")
async def login(email: str, password: str):
    token = create_token(email)
    return {"access_token": token,
            "token_type": "bearer"
            }

