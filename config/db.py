from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
import os
from typing import Annotated

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("Done creating tables")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]



"""
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1")) #type: ignore
    print("OK:", result.scalar()) #type: ignore

engine = create_engine(DATABASE_URL)
"""
