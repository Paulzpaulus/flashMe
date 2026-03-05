from sqlmodel import Session, select
from models.user import Users
from typing import Optional

def CRUD_get_all_users(session: Session) -> list[Users]:
    statement = select(Users)
    return list(session.exec(statement))

def CRUD_get_user(session: Session, id: int) -> Optional[Users]:
    return session.get(Users, id)

def CRUD_create_user(session: Session, user: Users) -> Users:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def CRUD_update_user(session: Session, id: int, new_email: Optional[str] = None, new_username: Optional[str] = None, new_password: Optional[str] = None) -> Users:
    user = session.get(Users, id)
    if not user:
        raise ValueError("User not found")
    if new_email:
        user.email = new_email
    if new_username:
        user.username = new_username
    if new_password:
        user.password = new_password
    session.commit()
    return user

def CRUD_delete_user(session: Session, user_id: int) -> Optional[Users]:
    user = session.get(Users, Users.id)
    if user:
        session.delete(user)
        session.commit()
    else:
        print("user not found")
    return user
