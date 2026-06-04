from fastapi import HTTPException, APIRouter, Depends
from sqlmodel import Session
from typing import cast

from models.user import Users
from service.user_CRUD import (
    CRUD_get_all_users,
    CRUD_get_user,
    CRUD_create_user,
    CRUD_update_user,
    CRUD_delete_user,
)
from config.db import get_session
from auth.auth import get_current_user, require_admin, hash_password
from schemas.user_schema import UserAdminCreate, UserRead, UserUpdate


user_routes = APIRouter(prefix="/users", tags=["Users"])


@user_routes.get(
    "/", response_model=list[UserRead], summary="List all users (admin only)"
)
async def get_users(
    session: Session = Depends(get_session),
    _: Users = Depends(require_admin),
):
    users = CRUD_get_all_users(session)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


@user_routes.get("/{user_id}", response_model=UserRead, summary="Get a user by ID")
async def show_a_user(
    user_id: int,
    session: Session = Depends(get_session),
    _: Users = Depends(get_current_user),
):
    user = CRUD_get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_routes.post(
    "/", response_model=UserRead, status_code=201, summary="Create a user (admin only)"
)
async def create_user(
    data: UserAdminCreate,
    session: Session = Depends(get_session),
    _: Users = Depends(require_admin),
):
    hashed_pw = hash_password(data.password)
    user = Users(
        name=data.name,
        email=data.email,
        hashed_password=hashed_pw,
        is_admin=data.is_admin,
    )
    return CRUD_create_user(session, user)


@user_routes.put(
    "/{user_id}",
    response_model=UserRead,
    summary="Update a user (own account or admin)",
)
async def edit_user(
    user_id: int,
    data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    if cast(int, current_user.id) != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="You can only edit your own account"
        )

    updates: dict = {}
    if data.name is not None:
        updates["name"] = data.name
    if data.email is not None:
        updates["email"] = data.email
    if data.password is not None:
        updates["hashed_password"] = hash_password(data.password)

    return CRUD_update_user(session, user_id, updates)


@user_routes.delete("/{user_id}", summary="Delete a user (own account or admin)")
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    if cast(int, current_user.id) != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="You can only delete your own account"
        )
    user = CRUD_delete_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted"}
