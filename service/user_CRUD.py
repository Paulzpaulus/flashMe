from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from models.user import Users
from typing import Optional
from exceptions import DuplicateEntryError, ResourceNotFoundError


def CRUD_get_all_users(session: Session) -> list[Users]:
    return list(session.exec(select(Users)))


def CRUD_get_user(session: Session, user_id: int) -> Optional[Users]:
    return session.get(Users, user_id)


def CRUD_create_user(session: Session, user: Users) -> Users:
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise DuplicateEntryError("Email already exists")
    session.refresh(user)
    return user


def CRUD_update_user(session: Session, user_id: int, updates: dict) -> Users:
    user = session.get(Users, user_id)
    if not user:
        raise ResourceNotFoundError("User not found")
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
