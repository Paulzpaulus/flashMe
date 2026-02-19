from sqlmodel import Session, select
from models.user import User
from typing import Optional

def CRUD_get_all_users(session: Session) -> Optional[list[User]]:
    return session.exec(User) #type: ignore

def CRUD_get_user(session: Session, id: int) -> Optional[User]:
    return session.get(User, id)

def CRUD_create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def CRUD_update_user(session: Session, id: int, new_email: Optional[str] = None, new_username: Optional[str] = None, new_password: Optional[str] = None) -> User:
    user = session.get(User, id)
    if not user:
        raise ValueError("User not found")
    if new_email:
        user.email = new_email
    if new_username:
        user.username = new_username
    if new_password:
        user.password = new_password  # Hashing how....?
    session.commit()
    return user

def CRUD_delete_user(session: Session, user_id: int) -> Optional[User]:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
    else:
        print("user not found")
    return user
