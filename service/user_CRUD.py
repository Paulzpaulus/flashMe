from sqlmodel import Session
from models.user_model import User
from typing import Optional

def get_all_users(session: Session) -> list[User]:
    return session.get(User)

def get_user(session: Session, user_id: int) -> User:
    return session.get(User, user_id)

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(session: Session, user_id: int, new_email: Optional[str] = None, new_username: Optional[str] = None, new_password: Optional[str] = None) -> User:
    user = session.get(User, user_id)
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

def delete_user(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
    return user
