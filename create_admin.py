import os
from dotenv import load_dotenv
from sqlmodel import Session, select
from config.db import engine
from models.user import Users
from pwdlib import PasswordHash

load_dotenv()


def create_admin() -> None:
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    name = os.getenv("ADMIN_NAME", "admin")

    if not email or not password:
        raise RuntimeError("ADMIN_EMAIL and ADMIN_PASSWORD must be set in .env")

    with Session(engine) as session:
        existing = session.exec(select(Users).where(Users.email == email)).first()
        if existing:
            print(f"Admin with email '{email}' already exists.")
            return

        hashed = PasswordHash.recommended().hash(password)
        admin = Users(name=name, email=email, hashed_password=hashed, is_admin=True)
        session.add(admin)
        session.commit()
        print(f"Admin '{name}' created successfully.")


if __name__ == "__main__":
    create_admin()
