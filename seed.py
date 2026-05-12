from sqlmodel import Session
from config.db import engine
from models.user import Users
from pwdlib import PasswordHash

def seed():
    password_hash = PasswordHash.recommended()

    with Session(engine) as session:
        hashed = password_hash.hash("test123")

        user = Users(
            name="Paula",
            email="test@web.de",
            hashed_password=hashed
        )

        session.add(user)
        session.commit()

    print("Seed user created.")

if __name__ == "__main__":
    seed()

