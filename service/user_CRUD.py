from sqlmodel import Session, select
from models.user import Users
from typing import Optional


def CRUD_get_all_users(session: Session) -> list[Users]:
    return list(session.exec(select(Users)))


def CRUD_get_user(session: Session, user_id: int) -> Optional[Users]:
    return session.get(Users, user_id)


def CRUD_create_user(session: Session, user: Users) -> Users:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def CRUD_update_user(session: Session, user_id: int, updates: dict) -> Users:
    user = session.get(Users, user_id)
    if not user:
        raise ValueError("User not found")
    for key, value in updates.items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user


def CRUD_delete_user(session: Session, user_id: int) -> Optional[Users]:
    user = session.get(Users, user_id)
    if user:
        session.delete(user)
        session.commit()
    return user
